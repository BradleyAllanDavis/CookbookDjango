# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class FoodGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class GramMapping(models.Model):
    ingredient = models.ForeignKey('Ingredient', models.CASCADE, blank=False)
    common_measure = models.CharField(max_length=128)
    amount_grams = models.FloatField()

    def __str__(self):
        return self.common_measure


class IngredientNutrient(models.Model):
    ingredient = models.ForeignKey('Ingredient', models.CASCADE)
    nutrient = models.ForeignKey('Nutrient', models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return str(self.ingredient) + " " + str(self.nutrient) + " " + str(
            self.amount)

    class Meta:
        unique_together = ('ingredient', 'nutrient')


class Ingredient(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    food_group = models.ForeignKey(FoodGroup, models.SET_NULL, null=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Nutrient(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    unit = models.CharField(max_length=64, blank=True, null=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name + " (" + self.measured_in + ")"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', models.CASCADE)
    amount = models.FloatField(null=False)
    unit = models.ForeignKey('GramMapping', models.CASCADE)

    def __str__(self):
        return str(self.amount) + " " + str(self.unit) + " " + str(
            self.ingredient)

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
    id = models.IntegerField(primary_key=True, blank=True)
    title = models.CharField(max_length=64, blank=True, null=False)
    description = models.CharField(max_length=2048, blank=True, null=True)
    instructions = models.CharField(max_length=2048, blank=True, null=True)
    serves = models.IntegerField()

    # Unneeded
    # is_private = models.BooleanField(blank=True)
    # parent_recipe = models.ForeignKey('Recipe', null=True, blank=True)
    # tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title


class SavedSearch(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    user = models.ForeignKey(User, models.CASCADE)
    search_name = models.CharField(max_length=64, blank=True, null=False)
    recipe_search_term = models.CharField(max_length=100, blank=True, null=True)
    ingredient_search_term = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.search_name


class SearchFoodGroup(models.Model):
    search = models.ForeignKey('SavedSearch', models.CASCADE)
    food_group = models.ForeignKey('FoodGroup', models.CASCADE)
    include = models.BooleanField()

    def __str__(self):
        return str(self.food_group) + " is in " + str(self.search)


class SearchTag(models.Model):
    search = models.ForeignKey('SavedSearch', models.CASCADE)
    tag = models.ForeignKey('Tag', models.CASCADE)
    include = models.BooleanField()

    def __str__(self):
        return str(self.tag) + " is in " + str(self.search)


class Tag(models.Model):
    tag_name = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.tag_name


class UserFavorite(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    recipe = models.ForeignKey('Recipe', models.CASCADE)

    def __str__(self):
        return str(self.recipe) + " was submitted by " + str(self.user)

    class Meta:
        unique_together = ('user', 'recipe')


class UserSubmission(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    recipe = models.ForeignKey('Recipe', models.CASCADE)

    def __str__(self):
        return str(self.recipe) + " is a favorite of " + str(self.user)

    class Meta:
        unique_together = ('user', 'recipe')


class RecipeTag(models.Model):
    recipe = models.ForeignKey('Recipe', models.CASCADE)
    tag = models.ForeignKey('Tag', models.CASCADE)

    def __str__(self):
        return str(self.recipe) + " has tag " + str(self.tag)


# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python
