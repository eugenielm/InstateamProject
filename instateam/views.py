from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView

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
    fields = ['first_name', 'last_name', 'email', 'phone', 'role']
    template_name = 'instateam/teammembers_cud.html'

    def get_success_url(self):
        return reverse('team_members_list')

    def get_form(self, *args):
        form = super().get_form(*args)
        form.fields['first_name'].widget.attrs['placeholder'] = 'first name'
        form.fields['last_name'].widget.attrs['placeholder'] = 'last name'
        form.fields['phone'].widget.attrs['placeholder'] = 'phone number - e.g. 111-222-3333'
        form.fields['email'].widget.attrs['placeholder'] = 'email'
        return form


class TeamMembersUpdate(UpdateView):
    model = TeamMember
    fields = ['first_name', 'last_name', 'email', 'phone', 'role']
    template_name = 'instateam/teammembers_cud.html'
    context_object_name = 'teammember'

    def get_success_url(self):
        return reverse('team_members_list')


def delete_teammember(request, pk):
    try:
        mb = TeamMember.objects.get(id=pk)
        mb.delete()
    # note for later: if exception, an error message should be displayed
    except: pass
    return redirect('team_members_list')