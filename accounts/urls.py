from django.conf.urls import patterns, url

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url': '/accounts/profile'}),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login$', 'login', {'template_name': 'accounts/login.html'}),
    url(r'^logout$', 'logout', {'next_page': '/ladders'}),
)

urlpatterns += patterns('accounts.views',
    url(r'^register$', 'register'),
    url(r'^profile$', 'profile'),
    url(r'^profile/edit$', 'edit_profile'),
)


