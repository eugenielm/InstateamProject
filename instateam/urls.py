from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path('^teammembers/?$', views.TeamMembersList.as_view(), name='team_members_list'),
]