from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns('',
    url(r'^$', login_required(TemplateView.as_view(template_name='stocks/index.html')), name='stocks'),
    url(r'^category$', login_required(views.CategoryList.as_view()), name='stocks_category_list'),
    url(r'^category/new$', login_required(views.CategoryCreate.as_view()), name='stocks_category_new'),
    url(r'^category/(?P<pk>\d+)/edit', login_required(views.CategoryUpdate.as_view()), name='stocks_category_edit'),
    url(r'^category/(?P<pk>\d+)/delete', login_required(views.CategoryDelete.as_view()), name='stocks_category_delete'),
    url(r'^master$', login_required(views.MasterList.as_view()), name='stocks_master_list'),
    url(r'^master/new$', login_required(views.MasterCreate.as_view()), name='stocks_master_new'),
    url(r'^master/(?P<pk>\d+)$', login_required(views.MasterDetail.as_view()), name='stocks_master_detail'),
    url(r'^master/(?P<pk>\d+)/edit$', login_required(views.MasterUpdate.as_view()), name='stocks_master_edit'),
    url(r'^master/(?P<pk>\d+)/delete$', login_required(views.MasterDelete.as_view()), name='stocks_master_delete'),
    url(r'^master/(?P<pk>\d+)/barcode_printing$', login_required(views.MasterBarcodePrinting.as_view()), name='stocks_master_barcode_printing')
)
