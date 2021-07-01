from django.contrib import admin
from api.models import Account, Profile, BusinessPartner, BusinessProfile

# Register your models here.
admin.site.register(Account)
admin.site.register(Profile)
admin.site.register(BusinessPartner)
admin.site.register(BusinessProfile)
