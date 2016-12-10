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
    # This needs the following view in the db:
    # CREATE VIEW cookbook_recipefoodgroups AS SELECT DISTINCT cookbook_recipeingredient.recipe_id, cookbook_ingredient.food_group_id FROM cookbook_recipeingredient,cookbook_ingredient WHERE cookbook_recipeingredient.id = cookbook_ingredient.id;

    results = Recipe.objects.raw(
        "SELECT * from cookbook_recipe WHERE cookbook_recipe.id IN (SELECT cookbook_recipetag.recipe_id FROM cookbook_recipetag WHERE cookbook_recipetag.tag_id IN (SELECT cookbook_searchtag.tag_id FROM cookbook_searchtag WHERE cookbook_searchtag.search_id = " + str(
            saved_search.id) + " UNION SELECT cookbook_recipefoodgroups.recipe_id::text FROM cookbook_recipefoodgroups WHERE cookbook_recipefoodgroups.food_group_id IN (SELECT cookbook_searchfoodgroup.food_group_id FROM cookbook_searchfoodgroup WHERE cookbook_searchfoodgroup.search_id = " + str(
            saved_search.id) + ")));")
    # force fetching results by looping, so we can safely delete the
    # temporary saved search object if needed
    recipes = []
    for recipe in results:
        recipes.append(recipe)
    results = recipes
    print("Result set length is " + str(len(results)))
    if len(results) == 0:
        results = None
    return results
