from django.db import models


class TeamMember(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    # A CharField that uses an EmailValidator for checking (max_length=254)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        # we assume the phone number will have the following format: xxx-yyy-zzzz
        max_length=12, 
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