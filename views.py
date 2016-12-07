from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from cookbook.models import Recipe, UserFavorite, SavedSearch, SearchFoodGroup, \
	FoodGroup, SearchTag, Tag
from cookbook.forms import SimpleSearchForm, AdvancedSearchForm


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
	return HttpResponse(template.render(context, request))


def advanced_recipe_search_results(request):
	recipe_name_search_term = request.GET.get("recipe_name_search_term")
	tags = request.GET.get("tags")
	food_groups = request.GET.get("food_groups")
	ingredient_name_search_term = request.GET.get("ingredient_name_search_term")

	# create the search object
	saved_search = SavedSearch(search_name="Recent search", user=request.user,
		recipe_search_term=recipe_name_search_term,
		ingredient_search_term=ingredient_name_search_term)
	saved_search.save()

	if food_groups:
		for food_group_id in food_groups:
			SearchFoodGroup(search=saved_search,
				food_group=FoodGroup.objects.get(pk=food_group_id),
				include=True).save()
	if tags:
		for tag_id in tags:
			SearchTag(search=saved_search, tag=Tag.objects.get(pk=tag_id),
				include=True).save()

	# execute the search
	# This needs the following view in the db:
	# CREATE VIEW cookbook_recipefoodgroups
	# AS SELECT DISTINCT
	# cookbook_recipeingredient.recipe_id, cookbook_ingredient.food_group_id
	# FROM cookbook_recipeingredient, cookbook_ingredient
	# WHERE
	# cookbook_recipeingredient.ingredient_id = cookbook_ingredient.ingredient_id;

	results = Recipe.objects.raw(
		"SELECT * from cookbook_recipe WHERE cookbook_recipe.id IN (SELECT cookbook_recipe_tags.recipe_id FROM cookbook_recipe_tags WHERE cookbook_recipe_tags.tag_id IN (SELECT cookbook_searchtag.tag_id FROM cookbook_searchtag WHERE cookbook_searchtag.search_id = " + str(saved_search.id) + " UNION SELECT cookbook_recipefoodgroups.recipe_id FROM cookbook_recipefoodgroups WHERE cookbook_recipefoodgroups.food_group_id IN (SELECT cookbook_searchfoodgroup.food_group_id FROM cookbook_searchfoodgroup WHERE cookbook_searchfoodgroup.search_id = " + str(saved_search.id) + ")));")

	print("length is " + str(len(list(results))))
	if len(list(results)) == 0:
		results = None

	template = loader.get_template('cookbook/search_results.html')
	context = {'search_results': results}
	add_common_context(context)
	return HttpResponse(template.render(context, request))


def create_account(request):
	return render(request, 'cookbook/create_user_account.html')


def add_common_context(other_context):
	other_context['simple_search_form'] = SimpleSearchForm()
	return other_context


def user_profile(request):
	template = loader.get_template('cookbook/user_profile.html')
	context = {}
	add_common_context(context)
	return HttpResponse(template.render(context, request))
