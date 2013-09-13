from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns('',
    url(r'^$', login_required(TemplateView.as_view(template_name='stocks/index.html'))),
)

urlpatterns += patterns('views',
    url(r'^masters/$', login_required(views.MasterList.as_view()), name='stocks_master_list'),
    url(r'^masters/new', login_required(views.MasterCreate.as_view()), name='stocks_master_new')
)
