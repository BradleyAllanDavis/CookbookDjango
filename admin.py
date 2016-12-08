from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from cookbook.models import UserFavorite, UserSubmission, FoodGroup, \
     GramMapping, IngredientNutrient, Ingredient, Nutrient, RecipeIngredient, \
     Recipe, SavedSearch, SearchFoodGroup, SearchTag, Tag, User

admin.site.register(UserFavorite)
admin.site.register(UserSubmission)
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
