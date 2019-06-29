from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path('^teammembers/?$', views.TeamMembersList.as_view(), 
        name='team_members_list'),
    re_path('^teammembers/new/?$', views.TeamMembersCreate.as_view(), 
        name='team_members_create'),
    re_path('^teammembers/(?P<pk>\d+)/edit/?$', views.TeamMembersUpdate.as_view(), 
        name='team_members_update'),
    re_path('^teammembers/(?P<pk>\d+)/delete/?$', views.delete_teammember, 
        name='team_members_delete'),
]