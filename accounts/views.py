from django.views import generic

from .models import *


class SectionIndexView(generic.ListView):
    model = Section
    template_name = 'accounts/sections/index.html'


class GroupIndexView(generic.ListView):
    model = Group
    template_name = 'accounts/groups/index.html'


class MasterIndexView(generic.ListView):
    model = Master
    template_name = 'accounts/masters/index.html'
