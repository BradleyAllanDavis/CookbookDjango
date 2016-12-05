# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior

from __future__ import unicode_literals

from django.db import models
from django.core.checks import Error, register


class FoodGroup(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class GramMapping(models.Model):
    ingredient = models.ForeignKey('Ingredient', blank=False)
    sequence_number = models.IntegerField(primary_key=True)
    amount_common_measure = models.FloatField()
    common_measure = models.CharField(max_length=128)
    amount_grams = models.FloatField()
    
    def __str__(self):
        if self.amount_common_measure != 1:
            return str(self.amount_common_measure) + " " + self.common_measure
        return self.common_measure

    class Meta:
        unique_together = ('ingredient', 'sequence_number')

class IngredientNutrient(models.Model):
    recipe_id = models.ForeignKey('Recipe')
    nutrient_id = models.ForeignKey('Nutrient')
    amount = models.FloatField()

    class Meta:
        unique_together = ('recipe_id','nutrient_id')


class Ingredient(models.Model):
    ingredient_id = models.IntegerField(primary_key=True, blank=True)
    food_group = models.ForeignKey(FoodGroup, models.DO_NOTHING)
    name = models.CharField(max_length=256)
    
    def __str__(self):
        return self.name


class LoggedInUser(models.Model):
    user_id = models.OneToOneField('User', models.CASCADE, primary_key=True)


class Nutrient(models.Model):
    nutrient_id = models.IntegerField(primary_key=True, blank=True, )
    measured_in = models.CharField(max_length=64, blank=True, null=True)
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name + " (" + self.measured_in + ")"

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', models.CASCADE)
    amount = models.FloatField(null=False)
    unit = models.ForeignKey('GramMapping', models.CASCADE)

    def __str__(self):
        return str(self.amount) + " " + str(self.unit) + " " + str(self.ingredient)
    
    # @classmethod
    # def check(self, **kwargs):
    #     errors = super(RecipeIngredient, self).check(**kwargs)
    #     passed = False
    #     for unit in self.unit.all():
    #         if unit.ingredient == self.ingredient:
    #             passed = True;
    #     if not passed:
    #         errors.append(Error("Unit "+str(self.unit+" is not valid for this Ingredient", 
    #         "Pick a unit listed in the Ingredient record", obj=self, 
    #         id="cookbook.E001"))
    #     return errors
            

class Recipe(models.Model):
    title = models.CharField(max_length=64, blank=True, null=False)
    description = models.CharField(max_length=2048, blank=True, null=True)
    instructions = models.CharField(max_length=2048, blank=True, null=True)
    is_private = models.BooleanField(blank=True)
    parent_recipe = models.ForeignKey('Recipe', null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    serves = models.IntegerField()

    def __str__(self):
        return self.title


class SavedSearch(models.Model):
    search_name = models.CharField(max_length=64, blank=True, null=False)
    user_id = models.ForeignKey('User', models.CASCADE, )

    def __str__(self):
        return self.search_name


class SearchFoodGroup(models.Model):
    search = models.ForeignKey('SavedSearch', models.DO_NOTHING)
    food_group = models.ForeignKey('FoodGroup', models.DO_NOTHING)
    include = models.BooleanField()

    def __str__(self):
        return str(self.food_group) + " (in " + str(self.search) + ")"


class SearchTag(models.Model):
    search = models.ForeignKey('SavedSearch', models.DO_NOTHING)
    tag = models.ForeignKey('Tag', models.DO_NOTHING)
    include = models.BooleanField()

    def __str__(self):
        return str(self.tag) + " (in " + str(self.search) + ")"


class Tag(models.Model):
    tag_name = models.CharField(primary_key=True, max_length=64, blank=True)

    def __str__(self):
        return self.tag_name


class User(models.Model):
    user_id = models.IntegerField(primary_key=True, blank=True)
    password = models.CharField(max_length=32)
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    favorite_recipes = models.ManyToManyField('Recipe', related_name='favorite_recipe')
    submitted_recipes = models.ManyToManyField('Recipe', related_name='submitted_recipe')

    def __str__(self):
        return self.first_name + " " + self.last_name
