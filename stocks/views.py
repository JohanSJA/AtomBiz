from django.views.generic import ListView

from .models import *


class MasterList(ListView):
    model = Master
