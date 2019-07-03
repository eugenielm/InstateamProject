import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

import phonenumbers
from phonenumber_field.modelfields import PhoneNumberField

class TeamMember(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    # A CharField that uses an EmailValidator for checking (max_length=254)
    email = models.EmailField(unique=True)
    # https://github.com/stefanfoulis/django-phonenumber-field
    phone = PhoneNumberField(
        # different users can't have the same phone number
        unique=True, 
        error_messages={'unique': 'This phone number is already associated with a member'})
    role = models.CharField(max_length=25, default='regular')

    def __repr__(self):
        return self.last_name + ', ' + self.first_name

    def __str__(self):
        return self.last_name + ', ' + self.first_name
    
    def get_fullname(self):
        return self.first_name + ' ' + self.last_name

    def is_admin(self):
        return self.role == 'admin'

    def formatted_phone_national(self):
        return phonenumbers.format_number(self.phone, phonenumbers.PhoneNumberFormat.NATIONAL)
    
    def formatted_phone_e164(self):
        return phonenumbers.format_number(self.phone, phonenumbers.PhoneNumberFormat.E164)

    def clean_fields(self, *args, **kwargs):
        # takes care of the email field validation and checks the presence of 
        # first/last name, phone, and role
        super().clean_fields(*args, **kwargs)
        errors = {}
        # make sure the first name is valid
        if not re.match("^[a-zA-Z\-\s']{1,60}$", getattr(self, 'first_name')):
            errors['first_name'] = "Please provide a valid first name."
        # make sure the last name is valid
        if not re.match("^[a-zA-Z\-\s']{1,60}$", getattr(self, 'last_name')):
            errors['last_name'] = "Please provide a valid last name."
        ### To be improved (?): first and last names should be allowed to contain accented characters
        
        if errors:
            raise ValidationError({
                k: ValidationError(_(v), code='invalid')\
                    for k,v in errors.items()
            })