from django.conf.urls import patterns, url
from blog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<entry_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<year>\d{4})/(?P<month>(?:\d{1}|\d{2}))$', views.month, name='month'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'index'}, name='logout'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^new_post/$', views.new_post, name='new_post'),
    url(r'^user/edit/$', views.edit_user_profile, name='edit_user_profile'),
    url(r'^user/update_about/$', views.update_about, name='update_about'),
    url(r'^user/update_email/$', views.update_email, name='update_email'),
    url(r'^user/(?P<username>[a-z0-9_-]+)/$', views.user_profile, name='user_profile'),
)
