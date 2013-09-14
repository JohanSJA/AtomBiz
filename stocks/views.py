from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from .models import *


class CategoryList(ListView):
    model = Category


class CategoryCreate(CreateView):
    model = Category
    success_url = reverse_lazy('stocks_category_list')


class CategoryUpdate(UpdateView):
    model = Category
    success_url = reverse_lazy('stocks_category_list')


class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('stocks_category_list')


class MasterList(ListView):
    model = Master


class MasterCreate(CreateView):
    model = Master
    success_url = reverse_lazy('stocks_master_list')


class MasterDetail(DetailView):
    model = Master


class MasterUpdate(UpdateView):
    model = Master
    success_url = reverse_lazy('stocks_master_list')


class MasterDelete(DeleteView):
    model = Master
    success_url = reverse_lazy('stocks_master_list')


class MasterBarcodePrinting(DetailView):
    model = Master
    template_name = 'stocks/master_barcode_printing.html'
