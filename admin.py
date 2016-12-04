from django.contrib import admin

# Register your models here.
from cookbook.models import FoodGroup, GramMappings, IngredientNutrients, Ingredients, Nutrients, RecipeIngredients, RecipeTags, Recipes, SavedSearches, SearchFoodGroups, SearchTags, Tags, UserFavorites, UserSubmittedRecipes, Users

admin.site.register(FoodGroup)
admin.site.register(GramMappings)
admin.site.register(IngredientNutrients)
admin.site.register(Ingredients)
admin.site.register(Nutrients)
admin.site.register(RecipeIngredients)
admin.site.register(RecipeTags)
admin.site.register(Recipes)
admin.site.register(SavedSearches)
admin.site.register(SearchFoodGroups)
admin.site.register(SearchTags)
admin.site.register(Tags)
admin.site.register(UserFavorites)
admin.site.register(UserSubmittedRecipes)
admin.site.register(Users)