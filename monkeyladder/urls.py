from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url': '/home/'}),
)

urlpatterns += patterns('',
    url(r'^home/$', 'monkeyladder.views.home'),
    url(r'^ladders/', include('core.urls')),
    url(r'^ladders/', include('matches.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
