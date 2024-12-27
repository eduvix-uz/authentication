from django.urls import path
from .views import verify_email, UserRegistrationView, UserLoginView, UserInfoView, UserUpdateView, UserDeleteView, UserUpdateProfileView, RequestPasswordResetView, PasswordResetConfirmView, LogoutUser

urlpatterns = [
    path('verify-email/<uuid:verification_code>/', verify_email, name='verify_email'),
    path('register/', UserRegistrationView, name='register'),
    path('login/', UserLoginView, name='login'),
    path('logout/', LogoutUser, name='logout'),
    path('update/<int:pk>/', UserUpdateProfileView, name='profile'),
    path('delete/<int:pk>/', UserUpdateProfileView, name='delete'),
    path('password-reset/', RequestPasswordResetView, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView, name='password_reset_confirm'),
    
    # urls for manager
    path('all-users/', UserInfoView, name='info'),
    path('manage/update/<int:pk>/', UserUpdateView, name='update'),
    path('manage/delete/<int:pk>/', UserDeleteView, name='delete'),

]