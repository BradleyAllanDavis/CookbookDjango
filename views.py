from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from cookbook.models import Recipe, UserFavorite
from cookbook.forms import SearchForm

def index(request):
    recipe_list = Recipe.objects.order_by('-id')[:5]
    template = loader.get_template('cookbook/index.html')
    context = {'recipe_list': recipe_list, 'simple_search_form' : SearchForm() }
    return HttpResponse(template.render(context, request))


def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    return HttpResponse(
		loader.get_template(
			'cookbook/detail.html').render(
				{'recipe': recipe,}, request))


def favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    user_favorite = UserFavorite(user=request.user, recipe=recipe)
    user_favorite.save() 
    print("user " + str(request.user) + " favorited recipe " + str(recipe))
    return HttpResponseRedirect(reverse('user_profile'))


def search_recipes(request):
    print(request.GET)
    search_term = request.GET.get("search_term")
    results = Recipe.objects.filter(title__contains=search_term)    
    template = loader.get_template('cookbook/search_results.html')
    context = {'search_results': results}
    return HttpResponse(template.render(context, request))

def advanced_recipe_search(request):
    print(request.GET)

def create_account(request):
    return render(request, 'cookbook/create_user_account.html')
