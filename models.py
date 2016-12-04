# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior

from __future__ import unicode_literals

from django.db import models


class FoodGroup(models.Model):
    food_group_id = models.IntegerField( primary_key=True, blank=True, null=True)
    name = models.CharField( max_length=64)


class GramMappings(models.Model):
    ingredient_id = models.IntegerField( primary_key=True)
    sequence_number = models.IntegerField( primary_key=True)
    amount_common_measure = models.FloatField()
    common_measure = models.CharField( max_length=128)
    amount_grams = models.FloatField()

    class Meta:
        unique_together = (('ingredient_id', 'sequence_number'),)


class IngredientNutrients(models.Model):
    ingredient_id = models.ForeignKey('Ingredients', models.DO_NOTHING, primary_key=True)
    nutrient_id = models.ForeignKey('Nutrients', models.DO_NOTHING, primary_key=True)
    amount = models.FloatField()
    
    class Meta:
        unique_together = (('ingredient_id', 'nutrient_id'),)


class Ingredients(models.Model):
    ingredient_id = models.IntegerField( primary_key=True, blank=True, null=True)
    food_group_id = models.ForeignKey(FoodGroup, models.DO_NOTHING, )
    name = models.CharField( max_length=256)


class LoggedInUsers:
    user_id = models.ForeignKey('Users', models.CASCADE, primary_key=True )


class Nutrients(models.Model):
    nutrient_id = models.IntegerField( primary_key=True, blank=True, null=True)
    unit = models.CharField( max_length=64, blank=True, null=True)
    name = models.CharField( max_length=128)

class RecipeIngredients:
    recipe_id = models.ForeignKey('Recipes', models.CASCADE, primary_key=True)
    ingredient_id = models.ForeignKey('Ingredients', models.CASCADE, primary_key=True)
    amount = models.FloatField(null=False)
    unit = models.ForeignKey('GramMappings', models.CASCADE, primary_key=True)
   
    class Meta:
        unique_together = (('recipe_id', 'ingredient_id'),)


class RecipeTags(models.Model):
    recipe_id = models.ForeignKey('Recipes', models.CASCADE, primary_key=True)
    tag_name = models.ForeignKey('Tags', models.CASCADE, primary_key=True)
    class Meta:
        unique_together = (('recipe_id', 'tag_name'),)


class Recipes:
    recipe_id = models.IntegerField( primary_key=True, blank=True, null=True)
    title = models.CharField(max_length=64, blank=True, null=False)
    description = models.CharField(max_length=2048, blank=True, null=True)
    instructions = models.CharField(max_length=2048, blank=True, null=True)
    is_private = models.BooleanField(blank=True, null=True)
    
    parent_recipe_id = models.ForeignKey('Recipes', models.CASCADE, primary_key=True)
    

class SavedSearches:
    search_id = models.IntegerField( primary_key=True, blank=True, null=True)
    search_name = models.CharField(max_length=64, blank=True, null=False)
    user_id = models.ForeignKey('Users', models.CASCADE, )


class SearchFoodGroups(models.Model):
    search_id = models.ForeignKey('SavedSearches', models.DO_NOTHING, primary_key=True)
    food_group_id = models.ForeignKey(FoodGroup, models.DO_NOTHING, primary_key=True)
    include = models.BooleanField()

    class Meta:
        unique_together = (('search_id', 'food_group_id'),)


class SearchTags(models.Model):
    search_id = models.ForeignKey('SavedSearches', models.DO_NOTHING, primary_key=True)
    tag_name = models.ForeignKey('Tags', models.DO_NOTHING, primary_key=True)
    include = models.BooleanField()

    class Meta:
        unique_together = (('search_id', 'tag_name'),)


class Tags(models.Model):
    tag_name = models.CharField( primary_key=True, max_length=64, blank=True, null=True)


class UserFavorites(models.Model):
    user_id = models.ForeignKey('Users', models.DO_NOTHING, primary_key=True)
    recipe_id = models.ForeignKey('Recipes', models.DO_NOTHING, primary_key=True)

    class Meta:
        unique_together = (('user_id', 'recipe_id'),)


class UserSubmittedRecipes(models.Model):
    user_id = models.ForeignKey('Users', models.DO_NOTHING, primary_key=True)
    user_id = models.ForeignKey('Recipe', models.DO_NOTHING, primary_key=True)
    
    class Meta:
        unique_together = (('user_id', 'recipe_id'),)
        
        
class Users(models.Model):
    user_id = models.IntegerField( primary_key=True, blank=True, null=True)
    password = models.CharField( max_length=32)
    first_name = models.CharField( max_length=32, blank=True, null=True)
    last_name = models.CharField( max_length=32, blank=True, null=True)
