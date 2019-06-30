from django import forms
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import TeamMember


def update_form(form):
    "Set the form's placeholders and radio checkboxes labels"
    form.fields['first_name'].widget.attrs['placeholder'] = 'first name'
    form.fields['last_name'].widget.attrs['placeholder'] = 'last name'
    form.fields['phone'].widget.attrs['placeholder'] = 'phone number - e.g. 111-222-3333'
    form.fields['email'].widget.attrs['placeholder'] = 'email'
    form.fields['role'].widget = forms.RadioSelect(choices=[
        ('regular', "Regular - Can't delete members"), 
        ('admin',  'Admin - Can delete members')
    ])
    return form


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

    def get_form(self, *args):
        form = super().get_form(*args)
        return update_form(form)

    def get_success_url(self):
        return reverse('team_members_list')


class TeamMembersUpdate(UpdateView):
    model = TeamMember
    fields = ['first_name', 'last_name', 'email', 'phone', 'role']
    template_name = 'instateam/teammembers_cud.html'
    context_object_name = 'teammember'

    def get_form(self, *args):
        form = super().get_form(*args)
        return update_form(form)

    def get_success_url(self):
        return reverse('team_members_list')


class TeamMembersDelete(DeleteView):
    model = TeamMember

    def get_success_url(self):
        return reverse('team_members_list')