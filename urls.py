from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^user_page/$', views.user_page, name='user_page'),
	url(r'^sign_in/$', views.sign_in, name='sign_in'),
	url(r'^advanced_search/$', views.advanced_search, name='advanced_search'),
	url(r'^readme/$', views.readme, name='readme'),
	url(r'^create_account/$', views.create_account, name='create_account'),
]
