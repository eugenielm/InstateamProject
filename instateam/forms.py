from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import TeamMember


class TeamMemberForm(forms.ModelForm):

    class Meta:
        model = TeamMember
        fields = ['first_name','last_name','email', 'phone', 'role']

    first_name = forms.CharField(
        max_length=60, 
        widget=forms.TextInput(attrs={'placeholder':'first name'})
    )
    last_name = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={'placeholder':'last name'})
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'email'}))
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder':'phone number'}))
    role = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=[
            ('regular', "Regular - Can't delete members"), 
            ('admin',  'Admin - Can delete members'),
        ],
        initial="regular",
    )