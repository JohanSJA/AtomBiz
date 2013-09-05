from django.views import generic

from .models import *


class SectionIndexView(generic.ListView):
    template_name = 'accounts/sections/index.html'
    context_object_name = 'section_list'

    def get_queryset(self):
        return Section.objects.all()


class GroupIndexView(generic.ListView):
    template_name = 'accounts/groups/index.html'
    context_object_name = 'group_list'

    def get_queryset(self):
        return Group.objects.all()


class MasterIndexView(generic.ListView):
    template_name = 'accounts/masters/index.html'
    context_object_name = 'master_list'

    def get_queryset(self):
        return Master.objects.all()
