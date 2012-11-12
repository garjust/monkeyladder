from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views.pages',
    url(r'^register/$', 'register_page'),
    url(r'^(?P<user_id>\d+)/profile/$', 'profile_page', name='profile_page'),
)

urlpatterns += patterns('accounts.views.content',
    url(r'^(?P<user_id>\d+)/info/$', 'user_info'),
    url(r'^(?P<user_id>\d+)/info/edit/$', 'edit_user_info'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'accounts/login_page.html'}, name='login'),
    url(r'^logout/$', 'logout', {'next_page': '/home/'}, name='logout'),
)
