from django.conf.urls import patterns, url

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url': '/accounts/profile/'}),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', 'logout', {'next_page': '/home/'}, name='logout'),
)

urlpatterns += patterns('accounts.views',
    url(r'^register/$', 'register', name='register'),
    url(r'^(?P<user_id>\d+)/profile/$', 'view_profile', name='view_profile'),
    url(r'^(?P<user_id>\d+)/profile/edit/$', 'edit_profile', name='edit_profile'),
)


