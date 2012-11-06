from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',
    url(r'^register/$', 'register_page'),
    url(r'^(?P<user_id>\d+)/profile/$', 'profile_page'),
    url(r'^(?P<user_id>\d+)/profile/edit/$', 'edit_profile_page'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'accounts/login_page.html'}, name='login'),
    url(r'^logout/$', 'logout', {'next_page': '/home/'}, name='logout'),
)
