from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<entry_id>\d+)/$', views.detail, name='detail')
)