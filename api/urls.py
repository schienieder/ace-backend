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
    GetBookingView,
    GetClientBookingView,
    DestroyEventBookingView,
    CreateInterviewView,
    GetInterviewView,
    DestroyInterviewView,
    CreateEventView,
    GetEventView,
    DestroyEventView,
    CreateAffiliationView,
    GetAffiliationView,
    UpdateRequestView,
    AllBusinessPartnersView,
    AllClientsView,
    AllClientBookingsView,
    AllEventsView,
    AllInterviewsView,
    AllAffiliationsView,
    AllRequestsView,
    AllAcceptedTasksView,
    AllEventTasksView,
    AllTasksView,
    AllCompletedTaskView,
    AdminGetPartnerView,
    AdminGetClientView,
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
    path("booking/<int:pk>", GetBookingView.as_view(), name="bookingView"),
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
    path("interview/<int:pk>", GetInterviewView.as_view(), name="interviewView"),
    path(
        "interview/destroy/<int:pk>",
        DestroyInterviewView.as_view(),
        name="interviewDestroy",
    ),
    # EVENT VIEW PATHS
    path("add_event/", CreateEventView.as_view(), name="createEvents"),
    path("event/<int:pk>", GetEventView.as_view(), name="eventView"),
    path("event/destroy/<int:pk>", DestroyEventView.as_view(), name="eventDestroy"),
    # AFFILIATIONS VIEW PATHS
    path("add_affiliation/", CreateAffiliationView.as_view(), name="createAffiliation"),
    path("affiliation/<int:pk>", GetAffiliationView.as_view(), name="affiliationView"),
    # LIST VIEW PATHS
    path(
        "partners_list/", AllBusinessPartnersView.as_view(), name="allBusinessPartners"
    ),
    path("clients_list/", AllClientsView.as_view(), name="allClients"),
    path("bookings_list/", AllClientBookingsView.as_view(), name="allBookings"),
    path("events_list/", AllEventsView.as_view(), name="allEvents"),
    path("interviews_list/", AllInterviewsView.as_view(), name="allInterviews"),
    path("affiliations_list/", AllAffiliationsView.as_view(), name="allAffiliations"),
    path(
        "requests_list/<int:pk>",
        AllRequestsView.as_view(),
        name="allPartnerRequests",
    ),
    path(
        "accepted_list/<int:pk>",
        AllAcceptedTasksView.as_view(),
        name="allAcceptedRequests",
    ),
    path(
        "event_tasks/<int:pk>",
        AllEventTasksView.as_view(),
        name="allEventTasks",
    ),
    path(
        "tasks_list/",
        AllTasksView.as_view(),
        name="allTasks",
    ),
    path(
        "completed_list/",
        AllCompletedTaskView.as_view(),
        name="allCompletedTasks",
    ),
    path("request_update/<int:pk>", UpdateRequestView.as_view(), name="requestUpdate"),
    # ADMIN VIEW PATHS
    path("admin_partner/<int:pk>", AdminGetPartnerView.as_view(), name="adminPartner"),
    path("admin_client/<int:pk>", AdminGetClientView.as_view(), name="adminClient"),
]
