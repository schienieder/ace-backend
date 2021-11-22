from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import (
    CreateAccountView,
    GetAccountView,
    GetClientProfileView,
    UpdateClientProfileView,
    DestroyClientProfileView,
    GetPartnerProfileView,
    UpdatePartnerProfileView,
    DestroyPartnerProfileView,
    CreateBookingView,
    GetClientBookingView,
    DestroyEventBookingView,
    CreateInterviewView,
    CreateEventView,
    AllBusinessPartnersView,
    AllClientsView,
    AllClientBookingsView,
    AllEventsView,
    AdminGetPartnerView,
)

urlpatterns = [
    path("register/", CreateAccountView.as_view(), name="registerAccount"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("account/<int:pk>", GetAccountView.as_view(), name="accountView"),
    # CLIENT VIEW PATHS
    path(
        "client_profile/<int:pk>",
        GetClientProfileView.as_view(),
        name="clientProfileView",
    ),
    path(
        "client_profile/update",
        UpdateClientProfileView.as_view(),
        name="clientProfileUpdate",
    ),
    path(
        "client_profile/destroy/<int:pk>",
        DestroyClientProfileView.as_view(),
        name="clientProfileDestroy",
    ),
    # PARTNER VIEW PATHS
    path(
        "partner_profile/<int:pk>",
        GetPartnerProfileView.as_view(),
        name="partnerProfileView",
    ),
    path(
        "partner_profile/update",
        UpdatePartnerProfileView.as_view(),
        name="partnerProfileUpdate",
    ),
    path(
        "partner_profile/destroy/<int:pk>",
        DestroyPartnerProfileView.as_view(),
        name="partnerProfileDestroy",
    ),
    # BOOKING VIEW PATHS
    path("add_booking/", CreateBookingView.as_view(), name="createBookings"),
    path(
        "client_booking/<int:pk>", GetClientBookingView.as_view(), name="clientBooking"
    ),
    path(
        "client_booking/destroy/<int:pk>",
        DestroyEventBookingView.as_view(),
        name="eventBookingDestroy",
    ),
    # INTERVIEW SCHEDULE VIEW PATHS
    path("add_interview/", CreateInterviewView.as_view(), name="createInterview"),
    # EVENT VIEW PATHS
    path("add_event/", CreateEventView.as_view(), name="createEvents"),
    # LIST VIEW PATHS
    path(
        "partners_list/", AllBusinessPartnersView.as_view(), name="allBusinessPartners"
    ),
    path("clients_list/", AllClientsView.as_view(), name="allClients"),
    path("bookings_list/", AllClientBookingsView.as_view(), name="allBookings"),
    path("events_list/", AllEventsView.as_view(), name="allEvents"),
    # ADMIN VIEW PATHS
    path("admin_partner/<int:pk>", AdminGetPartnerView.as_view(), name="adminPartner"),
]
