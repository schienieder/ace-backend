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
    ChatRoom,
    Chat,
    RoomMember,
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
admin.site.register(ChatRoom)
admin.site.register(Chat)
admin.site.register(RoomMember)
