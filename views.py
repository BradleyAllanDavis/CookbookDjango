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


def user_page(request):
	return render(request, 'cookbook/user_page.html')


def sign_in(request):
	return render(request, 'cookbook/sign_in.html')


def readme(request):
	return render(request, 'cookbook/readme.html')


def advanced_search(request):
	return render(request, 'cookbook/advanced_search.html')


def create_account(request):
	return render(request, 'cookbook/create_user_account.html')