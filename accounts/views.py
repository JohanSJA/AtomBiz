from django.views.generic import ListView

from .models import *


class SectionList(ListView):
    model = Section


class GroupList(ListView):
    model = Group


class MasterList(ListView):
    model = Master
