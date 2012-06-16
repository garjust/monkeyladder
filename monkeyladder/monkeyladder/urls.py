from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^ladders/$', 'ladders.views.index'),
    #url(r'^ladders/(?P<ladder_id>\d+)/$', 'ladders.views.detail'),
    #url(r'^ladders/(?P<ladder_id>\d+)/results/$', 'ladders.views.results'),
    #url(r'^ladders/(?P<ladder_id>\d+)/vote/$', 'ladders.views.vote'),

	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
 	url(r'^admin/', include(admin.site.urls)),
)
