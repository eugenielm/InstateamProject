from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import TeamMember
from .forms import TeamMemberForm


def index(request):
    return redirect('team_members_list')


class TeamMembersList(ListView):
    model = TeamMember
    context_object_name = 'team_members'
    queryset = TeamMember.objects.all()
    template_name = 'instateam/teammembers_list.html'


class TeamMembersCreate(CreateView):
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'instateam/teammembers_cud.html'
    success_url = reverse_lazy('team_members_list')


class TeamMembersUpdate(UpdateView):
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'instateam/teammembers_cud.html'
    context_object_name = 'teammember'
    success_url = reverse_lazy('team_members_list')


class TeamMembersDelete(DeleteView):
    model = TeamMember
    success_url = reverse_lazy('team_members_list')