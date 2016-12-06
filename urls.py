from django.conf.urls import include, url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^(?P<recipe_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
	url(r'^user_page/$', views.user_page, name='user_page'),
	url(r'^sign_in/$', views.sign_in, name='sign_in'),
	url(r'^advanced_search/$', views.advanced_search, name='advanced_search'),
	url(r'^readme/$', views.readme, name='readme'),
	url(r'^create_account/$', views.create_account, name='create_account'),
	url('^', include('django.contrib.auth.urls')),
    url(r'^accounts/profile/$', TemplateView.as_view(template_name='cookbook/user_profile.html'), name='user_profile'),

]
