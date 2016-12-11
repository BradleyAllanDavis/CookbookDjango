from django.conf.urls import include, url

from . import views

app_name = 'cookbook'
urlpatterns = [url(r'^$', views.index, name='index'),
    url(r'^(?P<recipe_id>[0-9]+)/$', views.recipe_detail, name='recipe_detail'),
    url(r'^(?P<recipe_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^advanced_search/$', views.advanced_recipe_search,
        name='advanced_search'),
    url(r'^create_user_account/$', views.create_user_account,
        name='create_user_account'),
    url(r'^saved_search_detail/(?P<saved_search_id>[0-9]+)$',
        views.saved_search_detail, name='saved_search_detail'),
    url(r'^save_search/$', views.save_search, name='save_search'),
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^saved_search_detail/(?P<saved_search_id>[0-9]+)/delete/$',
        views.delete_saved_search, name="delete_saved_search"),
    url(r'^tag_search/(?P<tag>.+)$', views.tag_search,
        name="tag_search"),
    url(r'^change_preferences/$', views.change_preferences,
        name='change_preferences')
]
# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python
