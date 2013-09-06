from django.views import generic

from .models import *


class MasterIndexView(generic.ListView):
    model = Master
    template_name = 'stocks/masters/index.html'
