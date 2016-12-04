# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior

from __future__ import unicode_literals

from django.db import models


class FoodGroup(models.Model):
    food_group_id = models.IntegerField(
        primary_key=True, blank=True, )
    name = models.CharField(max_length=64)


class GramMapping(models.Model):
    sequence_number = models.IntegerField(primary_key=True)
    amount_common_measure = models.FloatField()
    common_measure = models.CharField(max_length=128)
    amount_grams = models.FloatField()


class IngredientNutrient(models.Model):
    recipe_id = models.ForeignKey('Recipe')
    nutrient_id = models.ForeignKey('Nutrient')
    amount = models.FloatField()

    class Meta:
        unique_together = ('recipe_id','nutrient_id')


class Ingredient(models.Model):
    ingredient_id = models.IntegerField(
        primary_key=True, blank=True)
    food_group_id = models.ForeignKey(FoodGroup, models.DO_NOTHING, )
    measurements = models.ManyToManyField('GramMapping')
    name = models.CharField(max_length=256)


class LoggedInUser(models.Model):
    user_id = models.OneToOneField('User', models.CASCADE, primary_key=True)


class Nutrient(models.Model):
    nutrient_id = models.IntegerField(primary_key=True, blank=True, )
    measured_in = models.CharField(max_length=64, blank=True, null=True)
    name = models.CharField(max_length=128)


class RecipeIngredient(models.Model):
    recipe_id = models.ForeignKey('Recipe', models.CASCADE)
    ingredient_id = models.ForeignKey('Ingredient', models.CASCADE)
    amount = models.FloatField(null=False)
    unit = models.ForeignKey('GramMapping', models.CASCADE)

class Recipe(models.Model):
    recipe_id = models.IntegerField(primary_key=True, blank=True)
    title = models.CharField(max_length=64, blank=True, null=False)
    description = models.CharField(max_length=2048, blank=True, null=True)
    instructions = models.CharField(max_length=2048, blank=True, null=True)
    is_private = models.BooleanField(blank=True)
    food_group_id = models.ForeignKey('FoodGroup')
    parent_recipe_id = models.ForeignKey('Recipe')
    tags = models.ManyToManyField('Tag')


class SavedSearch(models.Model):
    search_id = models.IntegerField(primary_key=True, blank=True, )
    search_name = models.CharField(max_length=64, blank=True, null=False)
    user_id = models.ForeignKey('User', models.CASCADE, )


class SearchFoodGroup(models.Model):
    search_id = models.ForeignKey(
        'SavedSearch', models.DO_NOTHING)
    food_group_id = models.ForeignKey(
        'FoodGroup', models.DO_NOTHING)
    include = models.BooleanField()

class SearchTag(models.Model):
    search_id = models.ForeignKey('SavedSearch', models.DO_NOTHING)
    tag_name = models.ForeignKey('Tag', models.DO_NOTHING)
    include = models.BooleanField()


class Tag(models.Model):
    tag_name = models.CharField(primary_key=True, max_length=64, blank=True)


class User(models.Model):
    user_id = models.IntegerField(primary_key=True, blank=True)
    password = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    favorite_recipes = models.ManyToManyField('Recipe', related_name='favorite_recipe')
    submitted_recipes = models.ManyToManyField('Recipe', related_name='submitted_recipe')
