from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Account(AbstractUser):
    username = models.CharField(max_length = 55, unique = True)
    password = models.CharField(max_length = 55)
    REQUIRED_FIELDS = ['username', 'password']

class Client(models.model):
    first_name = models.CharField(max_length = 55)
    last_name = models.CharField(max_length = 55)
    mobile_number = models.IntegerField(unique = True)
    email = models.EmailField(max_length = 255, unique = True, null = True, blank = True)
    sex = models.IntegerField(null = True, blank = True)
    birthdate = models.DateField(null = True, blank = True)
    street_address = models.CharField(max_length = 255, blank = True)
    city = models.CharField(max_length = 55, blank = True)
    state_province = models.CharField(max_length = 55, blank = True) 
    postal_zip = models.IntegerField(null = True, blank = True)
    role = models.CharField(max_length = 10, blank = True)
    account = models.ForeignKey(
        Account, 
        on_delete = models.CASCADE
    )

class Partner(models.model):
    first_name = models.CharField(max_length = 55)
    last_name = models.CharField(max_length = 55)
    mobile_number = models.IntegerField(unique = True)
    email = models.EmailField(max_length = 255, unique = True, null = True, blank = True)
    business_name = models.CharField(max_length = 255, blank = True)
    type_of_business = models.CharField(max_length = 150, blank = True)
    street_address = models.CharField(max_length = 255, blank = True)
    city = models.CharField(max_length = 55, blank = True)
    state_province = models.CharField(max_length = 55, blank = True) 
    postal_zip = models.IntegerField(null = True, blank = True)
    role = models.CharField(max_length = 10, blank = True)
    account = models.ForeignKey(
        Account, 
        on_delete = models.CASCADE
    )

class Admin(models.Model):
    first_name = models.CharField(max_length = 55)
    last_name = models.CharField(max_length = 55)
    mobile_number = models.IntegerField(unique = True, null = True, blank = True)
    email = models.EmailField(max_length = 255, unique = True, null = True, blank = True)
    role = models.CharField(max_length = 10, blank = True)
    account = models.ForeignKey(
        Account, 
        on_delete = models.CASCADE
    )