from django.conf.urls import patterns, url

urlpatterns = patterns('loginbootstrap.views',
    url(r'^$', 'login'),
    url(r'^auth$', 'auth'),
)