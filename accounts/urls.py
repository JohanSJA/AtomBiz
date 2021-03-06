from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns('',
    url(r'^$', login_required(TemplateView.as_view(template_name='accounts/index.html'))),
    url(r'^sections/$', login_required(views.SectionList.as_view())),
    url(r'^groups/$', login_required(views.GroupList.as_view())),
    url(r'^masters/$', login_required(views.MasterList.as_view()))
)
