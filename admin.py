from django.contrib import admin

# Register your models here.
from cookbook.models import FoodGroup, GramMapping, IngredientNutrient, Ingredient, Nutrient, RecipeIngredient, Recipe, SavedSearch, SearchFoodGroup, SearchTag, Tag, User

admin.site.register(FoodGroup)
admin.site.register(GramMapping)
admin.site.register(IngredientNutrient)
admin.site.register(Ingredient)
admin.site.register(Nutrient)
admin.site.register(RecipeIngredient)

admin.site.register(Recipe)
admin.site.register(SavedSearch)
admin.site.register(SearchFoodGroup)
admin.site.register(SearchTag)
admin.site.register(Tag)
admin.site.register(User)
