from django.shortcuts import redirect
from django.views.generic import ListView

from .models import TeamMember


def index(request):
    return redirect('team_members_list')


class TeamMembersList(ListView):
    model = TeamMember
    context_object_name = 'team_members'
    queryset = TeamMember.objects.all()
    template_name = 'instateam/teammembers_list.html'