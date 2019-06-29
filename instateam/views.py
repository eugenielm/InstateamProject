from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView

from .models import TeamMember


def index(request):
    return redirect('team_members_list')


class TeamMembersList(ListView):
    model = TeamMember
    context_object_name = 'team_members'
    queryset = TeamMember.objects.all()
    template_name = 'instateam/teammembers_list.html'


class TeamMembersCreate(CreateView):
    model = TeamMember
    fields = ['first_name', 'last_name', 'email', 'phone']
    template_name = 'instateam/teammembers_create.html'

    def get_success_url(self):
        return reverse('team_members_list')