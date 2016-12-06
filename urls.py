from django.conf.urls import include, url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<recipe_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
	url(r'^advanced_search/$', TemplateView.as_view(template_name='cookbook/advanced_search.html'), name='advanced_search'),
	url(r'^search_recipes', views.search_recipes, name='search_recipes'),
	url(r'^create_account/$', views.create_account, name='create_account'),
        url(r'^profile/$', TemplateView.as_view(template_name='cookbook/user_profile.html'), name='user_profile'),
    url('^',include('django.contrib.auth.urls')),

]
