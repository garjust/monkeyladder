from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.views import auth_logout

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^ladders/', include('core.urls')),
    url(r'^ladders/', include('matches.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
