from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import (
    CreateAccountView,
    GetAccountView,
    GetAccountUsernameView,
    GetClientViaMobile,
    GetClientViaEmail,
    GetPartnerViaMobile,
    GetPartnerViaEmail,
    UpdateAccountView,
    GetClientProfileView,
    UpdateClientProfileView,
    DestroyClientProfileView,
    GetPartnerProfileView,
    UpdatePartnerProfileView,
    DestroyPartnerProfileView,
    CreateBookingView,
    GetBookingView,
    GetClientBookingView,
    UpdateBookingView,
    DestroyEventBookingView,
    CreateInterviewView,
    GetInterviewView,
    UpdateInterviewSchedule,
    DestroyInterviewView,
    CreateEventView,
    GetEventView,
    DashboardEvents,
    DashboardEventsSummary,
    GetClientEventView,
    ClientPayments,
    UpdateEventView,
    DestroyEventView,
    GetIncuredEvents,
    GetTotalSales,
    GetMonthlySales,
    CreateAffiliationView,
    GetAffiliationView,
    DashboardAffiliations,
    UpdateRequestView,
    DestroyRequestView,
    CreateRatingView,
    GetVenueForecast,
    GetCateringForecast,
    GetStylingForecast,
    GetMCForecast,
    GetPresentationForecast,
    GetCourtesyForecast,
    CreateChatRoom,
    GetChatRoom,
    JoinChatRoom,
    GetMemberRooms,
    DestroyChatRoom,
    PartnerDashboardEvents,
    PartnerDashboardAffiliations,
    PartnerTasksView,
    PartnerRequestsView,
    GetSalesYears,
    PresentTransactions,
    PastTransactions,
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
    AllChatRooms,
    AllRoomChatMessages,
    CreateTransaction,
    # email_view,
)

urlpatterns = [
    path("register/", CreateAccountView.as_view(), name="registerAccount"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("account/<int:pk>", GetAccountView.as_view(), name="accountView"),
    path(
        "check_username/<str:username>",
        GetAccountUsernameView.as_view(),
        name="checkUsername",
    ),
    path(
        "client_mobile/<str:mobile_number>",
        GetClientViaMobile.as_view(),
        name="checkClientMobile",
    ),
    path(
        "client_email/<str:email>",
        GetClientViaEmail.as_view(),
        name="checkClientEmail",
    ),
    path(
        "partner_mobile/<str:mobile_number>",
        GetPartnerViaMobile.as_view(),
        name="checkPartnerMobile",
    ),
    path(
        "partner_email/<str:email>",
        GetPartnerViaEmail.as_view(),
        name="checkPartnerEmail",
    ),
    path("account/update", UpdateAccountView.as_view(), name="updateAccount"),
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
    path("booking/update/<int:pk>", UpdateBookingView.as_view(), name="updateBooking"),
    path(
        "client_booking/destroy/<int:pk>",
        DestroyEventBookingView.as_view(),
        name="eventBookingDestroy",
    ),
    # INTERVIEW SCHEDULE VIEW PATHS
    path("add_interview/", CreateInterviewView.as_view(), name="createInterview"),
    path("interview/<int:pk>", GetInterviewView.as_view(), name="interviewView"),
    path(
        "interview/update/<int:pk>",
        UpdateInterviewSchedule.as_view(),
        name="updateInterview",
    ),
    path(
        "interview/destroy/<int:pk>",
        DestroyInterviewView.as_view(),
        name="interviewDestroy",
    ),
    # EVENT VIEW PATHS
    path("add_event/", CreateEventView.as_view(), name="createEvents"),
    path("event/<int:pk>", GetEventView.as_view(), name="eventView"),
    path("dashboard_events/", DashboardEvents.as_view(), name="dashboardEvents"),
    path(
        "events_summary/",
        DashboardEventsSummary.as_view(),
        name="dashboardEventsSummary",
    ),
    path(
        "partner_devents/",
        PartnerDashboardEvents.as_view(),
        name="partnerDashboardEvents",
    ),
    path("client_event/<int:pk>", GetClientEventView.as_view(), name="clientEvent"),
    path("client_payments/", ClientPayments.as_view(), name="clientPayments"),
    path("update_event/<int:pk>", UpdateEventView.as_view(), name="updateEvent"),
    path("event/destroy/<int:pk>", DestroyEventView.as_view(), name="eventDestroy"),
    path("incured_events/", GetIncuredEvents.as_view(), name="incuredEvents"),
    path(
        "total_sales/<str:transaction_year>", GetTotalSales.as_view(), name="totalSales"
    ),
    path(
        "monthly_sales/<str:transaction_year>",
        GetMonthlySales.as_view(),
        name="monthlySales",
    ),
    # AFFILIATIONS VIEW PATHS
    path("add_affiliation/", CreateAffiliationView.as_view(), name="createAffiliation"),
    path("affiliation/<int:pk>", GetAffiliationView.as_view(), name="affiliationView"),
    # path("dummy/", GetVenueForecast.as_view(), name="dummy"),
    path(
        "dashboard_affiliations/",
        DashboardAffiliations.as_view(),
        name="dashboardAffiliations",
    ),
    path(
        "partner_daffiliations/",
        PartnerDashboardAffiliations.as_view(),
        name="partnerDashboardAffiliations",
    ),
    path(
        "partner_tasks/",
        PartnerTasksView.as_view(),
        name="partnerTasks",
    ),
    path(
        "partner_requests/",
        PartnerRequestsView.as_view(),
        name="partnerRequests",
    ),
    path("request_update/<int:pk>", UpdateRequestView.as_view(), name="requestUpdate"),
    path(
        "request/destroy/<int:pk>", DestroyRequestView.as_view(), name="destroyRequest"
    ),
    # RATING VIEW PATHS
    path("add_rating/", CreateRatingView.as_view(), name="addRating"),
    # path("add_rating/<int:event_id>", CreateRatingView.as_view(), name="addRating"),
    path("venue_forecast/", GetVenueForecast.as_view(), name="venueForecast"),
    path("catering_forecast/", GetCateringForecast.as_view(), name="cateringForecast"),
    path("styling_forecast/", GetStylingForecast.as_view(), name="stylingForecast"),
    path("mc_forecast/", GetMCForecast.as_view(), name="mcForecast"),
    path(
        "presentation_forecast/",
        GetPresentationForecast.as_view(),
        name="presentationForecast",
    ),
    path(
        "courtesy_forecast/",
        GetCourtesyForecast.as_view(),
        name="coutesyForecast",
    ),
    # CHATROOM VIEWS
    path("new_chatroom/", CreateChatRoom.as_view(), name="newChatRoom"),
    path("chatroom/<str:room_key>", GetChatRoom.as_view(), name="getChatRoom"),
    path("join_chatroom/", JoinChatRoom.as_view(), name="joinChatRoom"),
    path("member_rooms/", GetMemberRooms.as_view(), name="memberRooms"),
    path(
        "chatroom/destroy/<str:room_key>",
        DestroyChatRoom.as_view(),
        name="destroyChatRoom",
    ),
    # TRANSACTION VIEW PATHS
    path(
        "sales_years/",
        GetSalesYears.as_view(),
        name="salesYears",
    ),
    path(
        "present_transactions/",
        PresentTransactions.as_view(),
        name="presentTransactions",
    ),
    path(
        "past_transactions/<str:year>",
        PastTransactions.as_view(),
        name="pastTransactions",
    ),
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
    path("chatroom_list/", AllChatRooms.as_view(), name="allChatRooms"),
    path("room_chats/<int:pk>", AllRoomChatMessages.as_view(), name="allRoomChats"),
    # ADMIN VIEW PATHS
    path("admin_partner/<int:pk>", AdminGetPartnerView.as_view(), name="adminPartner"),
    path("admin_client/<int:pk>", AdminGetClientView.as_view(), name="adminClient"),
    path("add_transaction/", CreateTransaction.as_view(), name="addTransaction"),
    # path("email_view", email_view, name="emailTemplate"),
]
