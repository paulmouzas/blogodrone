from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<entry_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})$', views.month, name='month'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': 'index'}, name='logout'),
    url(r'^login$', views.login, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^new_post$', views.new_post, name='new_post')
)
