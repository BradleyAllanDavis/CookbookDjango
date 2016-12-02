from __future__ import unicode_literals

from django.db import models


class TestRecipe(models.Model):
	recipe_id = models.IntegerField()
	title = models.CharField(max_length=64)
	description = models.CharField(max_length=2048)
	instructions = models.CharField(max_length=2048)
	is_private = models.BooleanField()

	def __str__(self):
		return self.title

# Create your models here.
