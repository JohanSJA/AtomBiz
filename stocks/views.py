from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .models import *


class MasterList(ListView):
    model = Master


class MasterCreate(CreateView):
    model = Master
    success_url = 'stocks_master_list'
