from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'atombiz.views.home', name='home'),
    # url(r'^atombiz/', include('atombiz.foo.urls')),
    url(r'^$', RedirectView.as_view(url='/users/login/')),

    url(r'^users/', include('users.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^stocks/', include('stocks.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
