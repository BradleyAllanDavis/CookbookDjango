from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from cookbook.forms import AdvancedSearchForm, SaveSearchForm, \
    NutritionPreferenceForm, CreateUserForm
from cookbook.methods import *
from cookbook.models import Recipe, UserFavorite, SavedSearch, \
    NutritionPreference, Nutrient, IngredientNutrient, Ingredient


def index(request):
    recipe_list = Recipe.objects.order_by('?')[:20]
    template = loader.get_template('cookbook/index.html')
    context = {'recipe_list': recipe_list}
    add_common_context(context)
    return HttpResponse(template.render(context, request))


def recipe_detail(request, recipe_id, error_message=None):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    recipe.instructions = recipe.instructions.replace("@newline@", "\n")
    context = {'recipe': recipe, 'error_message': error_message}

    if request.user.id:
        context["show_favorite_star"] = True
        try:
            UserFavorite.objects.get(user=request.user, recipe=recipe)
            context["favorite_star_filled"] = True
        except ObjectDoesNotExist:
            context["favorite_star_filled"] = False

        add_my_nutrients(context, recipe, request)

    add_nutrition_label_nutrients(context, recipe)

    # add other context
    add_common_context(context)
    template = loader.get_template('cookbook/recipe_detail.html')
    return HttpResponse(template.render(context, request))


def add_my_nutrients(context, recipe, request):
    my_nutrients = []
    for np in request.user.nutritionpreference_set.all():
        my_nutrients.append(np.nutrient)
    context["nutrients"] = amounts_for_nutrients_in_list(my_nutrients, recipe)


def add_nutrition_label_nutrients(context, recipe):
    # add nutrition info
    nutrition_label_nutrients = [Nutrient.objects.get(id=208),
        Nutrient.objects.get(id=204), Nutrient.objects.get(id=606),
        Nutrient.objects.get(id=605), Nutrient.objects.get(id=601),
        Nutrient.objects.get(id=307), Nutrient.objects.get(id=205),
        Nutrient.objects.get(id=291), Nutrient.objects.get(id=269),
        Nutrient.objects.get(id=203), Nutrient.objects.get(id=205), ]
    context["nutrition_label"] = amounts_for_nutrients_in_list(
        nutrition_label_nutrients, recipe)


def amounts_for_nutrients_in_list(nutrition_label_nutrients, recipe):
    nutrients = {}

    for ri in recipe.recipeingredient_set.all():
        for nutrient in nutrition_label_nutrients:
            try:
                inn = ri.ingredient.ingredientnutrient_set.get(
                    nutrient=nutrient)
                label = nutrient.nutrition_label_name()
                if label not in nutrients:
                    nutrients[label] = {
                        'name': nutrient.name, 'unit': nutrient.unit,
                        'amount': 0}
                amount_per_recipe = inn.amount / 100 * ri.amount * ri.gram_mapping.amount_grams
                amount_per_serving = amount_per_recipe / recipe.serves
                nutrients[label]['amount'] += amount_per_serving
            except IngredientNutrient.DoesNotExist:
                pass

    return nutrients


@login_required
def favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    try:
        user_favorite = UserFavorite.objects.get(user=request.user,
            recipe=recipe)
        user_favorite.delete()
    except UserFavorite.DoesNotExist:
        user_favorite = UserFavorite(user=request.user, recipe=recipe)
        user_favorite.save()

    args = {"recipe_id": recipe_id}
    return HttpResponseRedirect(reverse('cookbook:recipe_detail', kwargs=args))


def tag_search(request, tag):
    return HttpResponseRedirect(
        "/cookbook/advanced_search/?recipe_name_search_term=&ingredient_name_search_term=&tags=" + tag)


def foodgroup_search(request, foodgroup_id):
    return HttpResponseRedirect(
        "/cookbook/advanced_search/?recipe_name_search_term=&ingredient_name_search_term=&food_groups=" + foodgroup_id)


def ingredient_search(request, ingredient_id):
    return HttpResponseRedirect(
        "/cookbook/advanced_search/?recipe_name_search_term="
        "&ingredient_name_search_term=" + Ingredient.objects.get(
            pk=ingredient_id).name)


@login_required
def advanced_recipe_search(request):
    template = loader.get_template('cookbook/advanced_search.html')
    context = {'advanced_search_form': AdvancedSearchForm()}
    add_common_context(context)

    ingredient_name_search_term = request.GET.get("ingredient_name_search_term")
    recipe_name_search_term = request.GET.get("recipe_name_search_term")

    # need special handling for list-type parameters
    parameter_dictionary = dict(request.GET)
    if "tags" in parameter_dictionary:
        tags = parameter_dictionary["tags"]
    else:
        tags = []
    if "food_groups" in parameter_dictionary:
        food_groups = parameter_dictionary["food_groups"]
    else:
        food_groups = []

    if recipe_name_search_term or tags or food_groups or ingredient_name_search_term:
        search = create_saved_search(food_groups, ingredient_name_search_term,
            recipe_name_search_term, request, tags)
        params = {
            "ingredient_name_search_term": ingredient_name_search_term,
            "recipe_name_search_term": recipe_name_search_term, "tags": tags,
            "food_groups": food_groups}
        request.session["most_recent_search"] = params
        context['advanced_search_form'] = AdvancedSearchForm(initial=params)

        results = execute_saved_search(search)
        search.delete()
        print(results)

        # need to pass extra parameter to distinguish between 0 results and
        # didn't search yet
        if results:
            context["search_results"] = results
            # add save search form if there are results
            context["save_search_form"] = SaveSearchForm()
        else:
            context["no_matches"] = True

    return HttpResponse(template.render(context, request))


def save_search(request):
    most_recent_search_dict = request.session["most_recent_search"]
    if most_recent_search_dict:
        ingredient_name_search_term = most_recent_search_dict[
            "ingredient_name_search_term"]
        recipe_name_search_term = most_recent_search_dict[
            "recipe_name_search_term"]
        tags = most_recent_search_dict["tags"]
        food_groups = most_recent_search_dict["food_groups"]
        saved_search = create_saved_search(food_groups,
            ingredient_name_search_term, recipe_name_search_term, request, tags)
        saved_search.search_name = request.POST.get("saved_search_name")
        saved_search.save()
    return HttpResponseRedirect(reverse('cookbook:user_profile'))


@login_required
def change_preferences(request):
    if request.method == 'POST':
        # delete existing preferences
        for pref in NutritionPreference.objects.filter(user=request.user):
            pref.delete()

        nutrients = dict(request.POST)["nutrients"]
        for nutrient_id in nutrients:
            nutrient = Nutrient.objects.get(pk=nutrient_id)
            preference = NutritionPreference(user=request.user,
                nutrient=nutrient)
            preference.save()
        return HttpResponseRedirect(reverse('cookbook:index'))
    else:
        params = {
            "nutrients": [nutrientpref.nutrient.id for nutrientpref in
                request.user.nutritionpreference_set.all()]}
        form = NutritionPreferenceForm(initial=params)
        context = {"nutrition_preference_form": form}
        add_common_context(context)
        return render(request, 'cookbook/change_preferences.html', context)


def delete_saved_search(request, saved_search_id):
    saved_search = SavedSearch.objects.get(pk=saved_search_id)
    saved_search.delete()
    return HttpResponseRedirect(reverse('cookbook:user_profile'))


def create_user_account(request):
    if request.method == 'POST':
        try:
            User.objects.create_user(request.POST.get("username"),
                request.POST.get("email"), request.POST.get("password"))
            return HttpResponseRedirect(reverse('cookbook:login'))
        except IntegrityError:
            return HttpResponseRedirect(reverse("cookbook:username_exists"))
    else:
        context = {"create_user_form": CreateUserForm()}
        add_common_context(context)
        return render(request, 'cookbook/create_user_account.html', context)


def saved_search_detail(request, saved_search_id):
    saved_search = get_object_or_404(SavedSearch, pk=saved_search_id)
    context = {'saved_search': saved_search}
    add_common_context(context)
    template = loader.get_template("cookbook/saved_search_detail.html")
    return HttpResponse(template.render(context, request))


def add_most_favorited_ingredient(context, request):
    most_favorited_ingredient = Ingredient.objects.raw(
        "SELECT cookbook_ingredient.* FROM cookbook_ingredient INNER JOIN (SELECT cookbook_ingredient.id, "
        "count(*) as I_COUNT FROM (SELECT recipe_id FROM cookbook_usersubmission WHERE user_id = " + str(
            request.user.id) + "UNION SELECT recipe_id FROM cookbook_userfavorite WHERE user_id = " + str(
            request.user.id) + ") cr INNER JOIN cookbook_recipeingredient on cookbook_recipeingredient.recipe_id = cr.recipe_id INNER JOIN cookbook_ingredient on cookbook_ingredient.id = cookbook_recipeingredient.ingredient_id GROUP BY cookbook_ingredient.id ) ci on ci.id = cookbook_ingredient.id ORDER BY "
                               "I_COUNT desc LIMIT 1;")
    if len(list(most_favorited_ingredient)) == 0:
        ingredient = None
    else:
        ingredient = most_favorited_ingredient[0]
    context["most_favorited_ingredient"] = ingredient


def add_most_favorited_foodgroup(context, request):
    most_favorited_ingredient = Ingredient.objects.raw(
        "SELECT cookbook_ingredient.* FROM cookbook_ingredient INNER JOIN (SELECT cookbook_ingredient.id, "
        "count(*) as I_COUNT FROM (SELECT recipe_id FROM cookbook_usersubmission WHERE user_id = " + str(
            request.user.id) + "UNION SELECT recipe_id FROM cookbook_userfavorite WHERE user_id = " + str(
            request.user.id) + ") cr INNER JOIN cookbook_recipeingredient on cookbook_recipeingredient.recipe_id = cr.recipe_id INNER JOIN cookbook_ingredient on cookbook_ingredient.id = cookbook_recipeingredient.ingredient_id GROUP BY cookbook_ingredient.id ) ci on ci.id = cookbook_ingredient.id ORDER BY "
                               "I_COUNT desc LIMIT 1;")
    if len(list(most_favorited_ingredient)) == 0:
        foodgroup = None
    else:
        foodgroup = most_favorited_ingredient[0]
    context["most_favorited_foodgroup"] = foodgroup


def user_profile(request):
    template = loader.get_template('cookbook/user_profile.html')
    context = {}
    add_most_favorited_tag(context, request)
    add_most_favorited_ingredient(context, request)
    add_common_context(context)
    return HttpResponse(template.render(context, request))


def add_most_favorited_tag(context, request):
    most_favorited_tag = Tag.objects.raw("SELECT cookbook_tag.* FROM "
                                         "cookbook_tag INNER JOIN (SELECT cookbook_tag.tag_name, count(*) as T_COUNT FROM cookbook_userfavorite INNER "
                                         "JOIN cookbook_recipetag on cookbook_recipetag.recipe_id = cookbook_userfavorite.recipe_id INNER JOIN cookbook_tag on cookbook_recipetag.tag_id = cookbook_tag.tag_name WHERE cookbook_userfavorite.user_id = " + str(
        request.user.id) + " GROUP BY cookbook_tag.tag_name) ct on ct.tag_name = cookbook_tag.tag_name ORDER BY T_COUNT desc LIMIT 1;")
    if len(list(most_favorited_tag)) == 0:
        tag = None
    else:
        tag = most_favorited_tag[0]
    context["most_favorited_tag"] = tag

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python
