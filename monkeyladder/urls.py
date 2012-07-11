from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url': '/home/'}),
)

urlpatterns += patterns('',
    url(r'^home/$', 'monkeyladder.views.home'),
    url(r'^ladders/', include('core.urls')),
    url(r'^ladders/(?P<ladder_id>\d+)/', include('leaderboard.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),
)
