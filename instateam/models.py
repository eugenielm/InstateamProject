import re

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

import phonenumbers
from phonenumber_field.modelfields import PhoneNumberField


class TeamMember(models.Model):
    first_name = models.CharField(max_length=60, validators=[RegexValidator(
        regex="^[a-zA-Z\-\s']{1,60}$", 
        message="A first name can contain only letters, -, ' and white spaces.")])
    last_name = models.CharField(max_length=60, validators=[RegexValidator(
        regex="^[a-zA-Z\-\s']{1,60}$", 
        message="A last name can contain only letters, -, ' and white spaces.")])
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