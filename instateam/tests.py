from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from .models import TeamMember
from .forms import TeamMemberForm


class UrlsTestCase(TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = Client()
        self.default_attributes = {
            'first_name': 'Second',
            'last_name': 'Team Member',
            'phone': '4159374444',
            'email': 'second@example.com',
            'role': 'regular',
        }
    

    def setUp(self):
        mb = TeamMember.objects.create(
            first_name="Eugenie", 
            last_name="Le Moulec", 
            phone="4159375555", 
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


    def test_teammember_list_view(self):
        resp = self.client.get(reverse('team_members_list'))
        self.assertTemplateUsed(resp, 'instateam/teammembers_list.html')
        self.assertIs(resp.is_rendered, True)
        self.assertEqual(resp.context_data['object_list'].count(), 1)
        self.assertEqual(resp.context_data['object_list'].first().first_name, 'Eugenie')
        

    def test_teammember_add_view(self):
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


    def test_teammember_update_view(self):
        resp = self.client.get(reverse('team_members_update', kwargs={'pk': self.initial_member.id}))
        self.assertTemplateUsed(resp, 'instateam/teammembers_cud.html')
        self.assertIs(resp.is_rendered, True)
        # update the team member with no database contraint errors (unused phone, unused email)
        new_attrs = {
            'first_name': 'New Firstname',
            'last_name': 'New Lastname',
            'email': 'new@example.com',
            'phone': '4159376666',
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


    def test_teammember_delete_view(self):
        resp = self.client.post(
            reverse('team_members_delete', kwargs={'pk': self.initial_member.id}), 
            follow=True)
        self.assertEqual(resp.redirect_chain[-1], (reverse('team_members_list'), 302))
        # total count of Team members should be updated
        self.assertEqual(TeamMember.objects.all().count(), 0)


    def test_teammember_create(self):
        "Make sure unique and non-blank contraints are enforced when creating/updating a TeamMember instance"
        self.create_teammember(**self.default_attributes)
        # object instanciation with valid attributes except there's already a user with that email and phone
        mb = self.get_unsaved_teammember(**self.default_attributes)
        errors = False
        try:
            mb.full_clean()
        except ValidationError as e:
            self.assertTrue('phone' in e.message_dict)
            self.assertTrue('email' in e.message_dict)
            errors = True
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


    def test_teammember_phone_number_format(self):
        """Make sure the phone number can either be a valid US number with/without a country 
        prefix, or a valid international number with a country prefix."""
        attributes = self.default_attributes
        
        # US number with '+1' prefix (E164 format)
        attributes.update(phone='+14159374444')
        mb = self.get_unsaved_teammember(**attributes)
        try:
            mb.full_clean()
            errors = False
        except ValidationError:
            errors = True
        self.assertIs(errors, False)
        
        # 1 digit is missing
        attributes.update({'phone': '+1415937444'})
        mb = self.get_unsaved_teammember(**attributes)
        try:
            mb.full_clean()
            errors = False
        except ValidationError as e:
            self.assertTrue('phone' in e.message_dict)
            errors = True
        self.assertIs(errors, True)

        # international number with no country prefix
        attributes.update({'phone': '0296283522'})
        mb = self.get_unsaved_teammember(**attributes)
        errors = True
        try:
            mb.full_clean()
            errors = False
        except ValidationError as e:
            self.assertTrue('phone' in e.message_dict)
            errors = True
        self.assertIs(errors, True)

        # international number with a country prefix
        attributes.update({'phone': '+33296283522'})
        mb = self.get_unsaved_teammember(**attributes)
        errors = True
        try:
            mb.full_clean()
            errors = False
        except ValidationError:
            errors = True
        self.assertIs(errors, False)

        # US number with standard format
        attributes.update({'phone': '(415) 937-4468'})
        mb = self.get_unsaved_teammember(**attributes)
        try:
            mb.full_clean()
            errors = False
        except ValidationError:
            errors = True
        self.assertIs(errors, False)


    def test_teammember_form(self):
        "Test the TeamMemberForm"
        form_data = self.default_attributes.copy()
        form = TeamMemberForm(data=form_data)
        self.assertTrue(form.is_valid())

        # no first name
        form_data = self.default_attributes.copy()
        form_data['first_name'] = ''
        form = TeamMemberForm(data=form_data)
        self.assertFalse(form.is_valid())

        # invalid first name
        form_data = self.default_attributes.copy()
        form_data['first_name'] = 'John2'
        form = TeamMemberForm(data=form_data)
        self.assertFalse(form.is_valid())

        # no last name
        form_data = self.default_attributes.copy()
        form_data['last_name'] = ''
        form = TeamMemberForm(data=form_data)
        self.assertFalse(form.is_valid())

        # invalid last name
        form_data = self.default_attributes.copy()
        form_data['last_name'] = 'John2'
        form = TeamMemberForm(data=form_data)
        self.assertFalse(form.is_valid())

        # no email
        form_data = self.default_attributes.copy()
        form_data['email'] = ''
        form = TeamMemberForm(data=form_data)
        self.assertFalse(form.is_valid())

        # invalid email
        form_data = self.default_attributes.copy()
        form_data['email'] = 'John@example'
        form = TeamMemberForm(data=form_data)
        self.assertFalse(form.is_valid())

        # no phone number
        form_data = self.default_attributes.copy()
        form_data['phone'] = ''
        form = TeamMemberForm(data=form_data)
        self.assertFalse(form.is_valid())

        # invalid phone number
        form_data = self.default_attributes.copy()
        form_data['phone'] = '0666905410'
        form = TeamMemberForm(data=form_data)
        self.assertFalse(form.is_valid())

        # valid US phone number
        form_data = self.default_attributes.copy()
        form_data['phone'] = '415-937-4372'
        form = TeamMemberForm(data=form_data)
        self.assertTrue(form.is_valid())

        # valid international phone number
        form_data = self.default_attributes.copy()
        form_data['phone'] = '+33296283522'
        form = TeamMemberForm(data=form_data)
        self.assertTrue(form.is_valid())