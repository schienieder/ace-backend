from django.contrib import admin
from api.models import Account, Admin, Client, BusinessPartner, EventBookings, Event

# Register your models here.
admin.site.register(Account)
admin.site.register(Admin)
admin.site.register(Client)
admin.site.register(BusinessPartner)
admin.site.register(EventBookings)
admin.site.register(Event)
