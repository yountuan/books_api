from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from .views import PasswordResetRequestView, PasswordResetConfirmView, LoginView


urlpatterns = [
    path('api/register/', views.RegistrationView.as_view(), name='register'),
    path('api/activate/', views.ActivationView.as_view(), name='activate'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/password/reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('api/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
