from django.urls import path
from .views import *

app_name = 'books'

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/logout/', LogoutView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('api/user-detail/', CustomUserView.as_view(), name='user-detail'),
    path('add-to-wishlist/<int:book_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:book_id>/', remove_from_wishlist, name='remove_from_wishlist'),


]