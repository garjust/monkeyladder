from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^ladders/$', 'ladders.views.collection'),
    url(r'^ladders/(?P<ladder_id>\d+)/$', 'ladders.views.element'),
    url(r'^ladders/(?P<ladder_id>\d+)/change/$', 'ladders.views.change'),

	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
 	url(r'^admin/', include(admin.site.urls)),
)
