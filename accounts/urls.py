from django.conf.urls import patterns, url

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url': '/accounts/profile/'}),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'accounts/login_page.html'}, name='login'),
    url(r'^logout/$', 'logout', {'next_page': '/home/'}, name='logout'),
)

urlpatterns += patterns('accounts.views',
    url(r'^register/$', 'register_page', name='register'),
    url(r'^(?P<user_id>\d+)/profile/$', 'profile_page', name='view_profile'),
    url(r'^(?P<user_id>\d+)/profile/edit/$', 'edit_profile_page', name='edit_profile'),
)
