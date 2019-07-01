from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from .models import TeamMember


class UrlsTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = Client()
        self.default_attributes = {
            'first_name': 'Second',
            'last_name': 'Team Member',
            'phone': '000-111-2222',
            'email': 'second@example.com',
            'role': 'regular',
        }
    

    def setUp(self):
        mb = TeamMember.objects.create(
            first_name="Eugenie", 
            last_name="Le Moulec", 
            phone="111-222-3333", 
            email="eugenie@example.com")
        self.initial_member = mb


    def create_teammember(self, **kwargs):
        return TeamMember.objects.create(**kwargs)


    def get_unsaved_teammember(self, **kwargs):
        return TeamMember(**kwargs)


    def test_main_index_view(self):
        resp = self.client.get(reverse('index'), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.redirect_chain[-1], (reverse('team_members_list'), 302))


    def test_list_view(self):
        resp = self.client.get(reverse('team_members_list'))
        self.assertTemplateUsed(resp, 'instateam/teammembers_list.html')
        self.assertIs(resp.is_rendered, True)
        self.assertEqual(resp.context_data['object_list'].count(), 1)
        self.assertEqual(resp.context_data['object_list'].first().first_name, 'Eugenie')
        

    def test_add_view(self):
        resp = self.client.get(reverse('team_members_create'))
        self.assertTemplateUsed(resp, 'instateam/teammembers_cud.html')
        self.assertIs(resp.is_rendered, True)
        # create a team member with no database contraint errors (unused phone, unused email)
        resp2 = self.client.post(reverse('team_members_create'), self.default_attributes, follow=True)
        self.assertEqual(resp2.redirect_chain[-1], (reverse('team_members_list'), 302))
        self.assertEqual(TeamMember.objects.all().count(), 2)
        # create a team member with already used phone and email
        resp3 = self.client.post(reverse('team_members_create'), self.default_attributes)
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(TeamMember.objects.all().count(), 2)


    def test_update_view(self):
        resp = self.client.get(reverse('team_members_update', kwargs={'pk': self.initial_member.id}))
        self.assertTemplateUsed(resp, 'instateam/teammembers_cud.html')
        self.assertIs(resp.is_rendered, True)
        # update the team member with no database contraint errors (unused phone, unused email)
        new_attrs = {
            'first_name': 'New Firstname',
            'last_name': 'New Lastname',
            'email': 'new@example.com',
            'phone': '999-888-7777',
            'role': 'regular',
        }
        resp2 = self.client.post(
            reverse('team_members_update', kwargs={'pk': self.initial_member.id}), 
            new_attrs, follow=True)
        self.assertEqual(resp2.redirect_chain[-1], (reverse('team_members_list'), 302))
        # total count of Team members shouldn't change
        self.assertEqual(TeamMember.objects.all().count(), 1)
        
        # update self.initial_member with already used phone and email - first create another team member
        self.create_teammember(**self.default_attributes)
        resp3 = self.client.post(
            reverse('team_members_update', kwargs={'pk': self.initial_member.id}), 
            self.default_attributes)
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(TeamMember.objects.all().count(), 2)


    def test_delete_view(self):
        resp = self.client.post(
            reverse('team_members_delete', kwargs={'pk': self.initial_member.id}), 
            follow=True)
        self.assertEqual(resp.redirect_chain[-1], (reverse('team_members_list'), 302))
        # total count of Team members should be updated
        self.assertEqual(TeamMember.objects.all().count(), 0)


    def test_create_teammember(self):
        "Make sure unique and non-blank contraints are enforced when creating/updating a TeamMember instance"
        self.create_teammember(**self.default_attributes)
        # object instanciation without saving - with the same attributes as the obj instantiated above
        mb = self.get_unsaved_teammember(**self.default_attributes)
        errors = True
        try:
            mb.full_clean()
            errors = False
        except ValidationError as e:
            self.assertTrue('phone' in e.message_dict)
            self.assertTrue('email' in e.message_dict)
        self.assertIs(errors, True)
        
        # create member with empty fields
        mb2 = self.get_unsaved_teammember(first_name='', last_name='', email='', phone='')
        try:
            mb2.full_clean()
            errors = False
        except ValidationError as e:
            self.assertTrue('first_name' in e.message_dict)
            self.assertTrue('last_name' in e.message_dict)
            self.assertTrue('phone' in e.message_dict)
            self.assertTrue('email' in e.message_dict)
        self.assertIs(errors, True)