from django.conf.urls import include, url

from . import views

app_name = 'cookbook'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<recipe_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
	url(r'^advanced_search/$', views.advanced_recipe_search, name='advanced_search'),
	url(r'^advanced_recipe_search_results', views.advanced_recipe_search_results, name='advanced_recipe_search_results'),
	url(r'^recipe_search_results', views.recipe_search_results, name='search_recipes'),
	url(r'^create_user_account/$', views.create_user_account, name='create_user_account'),
	url(r'^saved_search_detail/$', views.saved_search_detail, name='saved_search_detail'),
	url(r'^profile/$', views.user_profile, name='user_profile'),
	url('^', include('django.contrib.auth.urls')),
]
# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python
