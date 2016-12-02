from django.http import HttpResponse
from django.shortcuts import render


def index(request):
	return HttpResponse("This is the cookbook index.")


def detail(request, recipe_id):
	return HttpResponse("You're look at recipe %s." % recipe_id)

