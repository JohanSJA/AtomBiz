from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns('',
    url(r'^$', login_required(TemplateView.as_view(template_name='stocks/index.html'))),
    url(r'^masters/$', login_required(views.MasterIndexView.as_view()))
)
