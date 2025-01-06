from django.urls import path
from .views import verify_email, UserRegistrationView, UserLoginView, UserUpdateProfileView, RequestPasswordResetView, PasswordResetConfirmView, LogoutUser, set_csrf_cookie

urlpatterns = [
    path('verify-email/<uuid:verification_code>/', verify_email, name='verify_email'),
    path('register/', UserRegistrationView, name='register'),
    path('login/', UserLoginView, name='login'),
    path('logout/', LogoutUser, name='logout'),
    path('control/<int:pk>/', UserUpdateProfileView, name='control'),
    path('password-reset/', RequestPasswordResetView, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView, name='password_reset_confirm'),
    path("set-csrf-cookie/", set_csrf_cookie, name="set-csrf-cookie"),
]