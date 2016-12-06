from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from cookbook.models import Recipe, UserFavorite


def index(request):
    recipe_list = Recipe.objects.order_by('-id')[:5]
    template = loader.get_template('cookbook/index.html')
    context = {'recipe_list': recipe_list}
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


def advanced_search(request):
    return render(request, 'cookbook/advanced_search.html')


def create_account(request):
    return render(request, 'cookbook/create_user_account.html')
