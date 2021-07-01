from django.urls import path
from api.views import CreateAccountView

urlpatterns = [
    path('register/', CreateAccountView.as_view(), name = 'registerAccount')
]