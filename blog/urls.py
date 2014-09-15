from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<entry_id>\d+)/$', views.detail, name='detail'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': 'index'}),
    url(r'^login$', views.login),
    url(r'^signup$', views.signup)
)