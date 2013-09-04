from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'users/login.html'}),
    url(r'^logout/$', 'logout_then_login'),
)

urlpatterns += patterns('.views',
    url(r'^dashboard/$', login_required(TemplateView.as_view(template_name='users/dashboard.html')))
)
