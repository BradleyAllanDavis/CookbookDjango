from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from cookbook.forms import AdvancedSearchForm, SaveSearchForm
from cookbook.methods import *
from cookbook.models import Recipe, UserFavorite, SavedSearch


def index(request):
    recipe_list = Recipe.objects.order_by('-id')[:5]
    template = loader.get_template('cookbook/index.html')
    context = {'recipe_list': recipe_list}
    add_common_context(context)
    return HttpResponse(template.render(context, request))


def detail(request, recipe_id, error_message=None):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {'recipe': recipe, 'error_message': error_message}
    add_common_context(context)

    return HttpResponse(
        loader.get_template('cookbook/detail.html').render(context, request))


def favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    user_favorite = UserFavorite(user=request.user, recipe=recipe)
    try:
        user_favorite.save()
        print("user " + str(request.user) + " favorited recipe " + str(recipe))
        return HttpResponseRedirect(reverse('cookbook:user_profile'))
    except IntegrityError as e:
        return detail(request, recipe_id, error_message=str(e))


def recipe_search_results(request):
    search_term = request.GET.get("search_term")
    results = Recipe.objects.filter(title__contains=search_term)
    template = loader.get_template('cookbook/search_results.html')
    context = {'search_results': results}
    add_common_context(context)

    return HttpResponse(template.render(context, request))


def advanced_recipe_search(request):
    template = loader.get_template('cookbook/advanced_search.html')
    context = {'advanced_search_form': AdvancedSearchForm()}
    add_common_context(context)

    ingredient_name_search_term = request.GET.get("ingredient_name_search_term")
    recipe_name_search_term = request.GET.get("recipe_name_search_term")
    tags = request.GET.get("tags")
    food_groups = request.GET.get("food_groups")

    if recipe_name_search_term or tags or food_groups or ingredient_name_search_term:
        search = create_saved_search(food_groups, ingredient_name_search_term,
            recipe_name_search_term, request, tags)
        request.session["most_recent_search"] = {
            "ingredient_name_search_term": ingredient_name_search_term,
            "recipe_name_search_term": recipe_name_search_term, "tags": tags,
            "food_groups": food_groups}

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


def create_user_account(request):
    return render(request, 'cookbook/create_user_account.html')


def saved_search_detail(request, saved_search_id):
    saved_search = get_object_or_404(SavedSearch, pk=saved_search_id)
    context = {'saved_search': saved_search}
    add_common_context(context)
    template = loader.get_template("cookbook/saved_search_detail.html")
    return HttpResponse(template.render(context, request))


def add_common_context(other_context):
    other_context['simple_search_form'] = SimpleSearchForm()
    return other_context


def user_profile(request):
    template = loader.get_template('cookbook/user_profile.html')
    context = {}
    add_common_context(context)
    return HttpResponse(template.render(context, request))

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python
