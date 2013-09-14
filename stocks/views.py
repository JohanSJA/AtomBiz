from django.views.generic import ListView
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
    success_url = 'stocks_master_list'
