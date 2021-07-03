from django.contrib import admin
from api.models import Account, Profile, BusinessPartner

# Register your models here.
admin.site.register(Account)
admin.site.register(Profile)
admin.site.register(BusinessPartner)
