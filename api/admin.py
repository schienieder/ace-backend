from django.contrib import admin
from api.models import (
    Account,
    Admin,
    Client,
    BusinessPartner,
    EventBookings,
    Event,
    InterviewSchedule,
    AffiliationRequest,
    Rating,
    ClientRoom,
    PartnerRoom,
    GroupRoom,
    ClientGroupRoom,
)

# Register your models here.
admin.site.register(Account)
admin.site.register(Admin)
admin.site.register(Client)
admin.site.register(BusinessPartner)
admin.site.register(EventBookings)
admin.site.register(Event)
admin.site.register(InterviewSchedule)
admin.site.register(AffiliationRequest)
admin.site.register(Rating)
admin.site.register(ClientRoom)
admin.site.register(PartnerRoom)
admin.site.register(GroupRoom)
admin.site.register(ClientGroupRoom)
