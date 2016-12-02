from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from cookbook.models import TestRecipe


def index(request):
	recipe_list = TestRecipe.objects.order_by('-recipe_id')[:5]
	template = loader.get_template('cookbook/index.html')
	context = {
		'recipe_list': recipe_list, }
	return HttpResponse(template.render(context, request))


def detail(request, recipe_id):
	try:
		recipe = TestRecipe.objects.get(pk=recipe_id)
	except TestRecipe.DoesNotExist:
		raise Http404("Recipe does not exist")
	return render(request, 'cookbook/detail.html', {'recipe': recipe})
