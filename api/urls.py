from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import (
    CreateAccountView,
    GetAccountView,
    GetClientProfileView,
    GetPartnerProfileView,
    AllBusinessPartnersView,
    AllClientsView,
)

urlpatterns = [
    path("register/", CreateAccountView.as_view(), name="registerAccount"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("account/<int:pk>", GetAccountView.as_view(), name="accountView"),
    path(
        "partner_profile/<int:pk>",
        GetPartnerProfileView.as_view(),
        name="partnerProfileView",
    ),
    path(
        "client_profile/<int:pk>",
        GetClientProfileView.as_view(),
        name="clientProfileView",
    ),
    path(
        "partners_list/", AllBusinessPartnersView.as_view(), name="allBusinessPartners"
    ),
    path("clients_list/", AllClientsView.as_view(), name="allClients"),
]
