from cookbook.forms import SimpleSearchForm
from cookbook.models import SavedSearch, SearchFoodGroup, FoodGroup, SearchTag, \
    Recipe, Tag


def add_common_context(other_context):
    other_context['simple_search_form'] = SimpleSearchForm()
    return other_context


def create_saved_search(food_groups, ingredient_name_search_term,
                        recipe_name_search_term, request, tags):
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
        for tag in tags:
            SearchTag(search=saved_search, tag=Tag.objects.get(pk=tag),
                include=True).save()

    return saved_search


def execute_saved_search(saved_search):
    results = Recipe.objects.raw(
        "SELECT * FROM (SELECT DISTINCT cookbook_recipe.* FROM cookbook_recipe INNER JOIN cookbook_recipetag ON cookbook_recipetag.recipe_id = cookbook_recipe.id INNER JOIN cookbook_recipeingredient ON cookbook_recipeingredient.recipe_id = cookbook_recipe.id INNER JOIN cookbook_ingredient ON cookbook_ingredient.id = cookbook_recipeingredient.ingredient_id INNER JOIN cookbook_foodgroup ON cookbook_foodgroup.id = "
        "cookbook_ingredient.food_group_id WHERE CASE WHEN (SELECT CASE WHEN recipe_search_term is not null THEN True ELSE False END FROM cookbook_savedsearch WHERE id = " + str(saved_search.id) + ") THEN cookbook_recipe.title like '%' || (SELECT recipe_search_term FROM cookbook_savedsearch WHERE id = " + str(saved_search.id) + ") || '%' ELSE True END AND CASE  WHEN (SELECT CASE WHEN ingredient_search_term is not null THEN True ELSE False END FROM cookbook_savedsearch WHERE id = " + str(saved_search.id) + ") THEN cookbook_ingredient.name like '%' || (SELECT ingredient_search_term FROM cookbook_savedsearch WHERE id = " + str(saved_search.id) + ") || '%' ELSE True END AND CASE WHEN (SELECT CASE WHEN count(*) > 0 THEN True ELSE False END FROM cookbook_searchfoodgroup WHERE id = " + str(saved_search.id) + " AND include = 't') THEN cookbook_ingredient.food_group_id in (SELECT food_group_id FROM cookbook_searchfoodgroup WHERE id = " + str(saved_search.id) + " AND include = 't') ELSE True END AND CASE WHEN (SELECT CASE WHEN count(*) > 0 THEN True ELSE False END FROM cookbook_searchfoodgroup WHERE id = " + str(saved_search.id) + " AND include = 'f') THEN cookbook_ingredient.food_group_id not in (SELECT food_group_id FROM cookbook_searchfoodgroup WHERE id = " + str(saved_search.id) + " AND include = 'f') ELSE True END AND CASE WHEN (SELECT CASE WHEN count(*) > 0 THEN True ELSE False END FROM cookbook_searchtag WHERE id = " + str(saved_search.id) + " AND include = 't') THEN cookbook_recipetag.tag_id in (SELECT tag_id FROM cookbook_searchtag WHERE id = " + str(saved_search.id) + " and include = 't') ELSE True END AND CASE WHEN (SELECT CASE WHEN count(*) > 0 THEN True ELSE False END FROM cookbook_searchtag WHERE id = " + str(saved_search.id) + " AND include = 'f') THEN cookbook_recipetag.tag_id not in (SELECT tag_id FROM cookbook_searchtag WHERE id = " + str(saved_search.id) + " and include = 'f') ELSE True END LIMIT 5);")

    # force fetching results by looping, so we can safely delete the
    # temporary saved search object if needed
    recipes = []
    for i in range(min(len(list(results)), 50)):
        recipes.append(results[i])
    results = recipes
    print("Result set length is " + str(len(results)))
    if len(results) == 0:
        results = None
    return results
