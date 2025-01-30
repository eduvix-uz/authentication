from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from users.models import EmailVerification
from users.services.Clients.Views.RegisterUser import UserRegistrationView
from users.services.Clients.Views.LoginUser import UserLoginView
from users.services.Clients.Views.UpdateDeleteUser import UserUpdateProfileView
from users.services.Clients.Views.RequestResetPassword import RequestPasswordResetView
from users.services.Clients.Views.ConfirmResetPassword import PasswordResetConfirmView
from users.services.Clients.Views.LogoutUser import LogoutUser
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response


# Verify email
@api_view(['GET'])
def verify_email(request, verification_code):
    try:
        verification_record = EmailVerification.objects.get(verification_code=verification_code)
        user = verification_record.user
        user.is_verified = True
        user.save()
        send_mail(
                    subject="prohub.uz platformasiga xush kelibsiz!",
                    message=(
                        f"Hurmatli {user.first_name} {user.last_name} siz muvaffaqiyatli ro'yxatdan o'tdingiz! \n\n"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
        verification_record.delete()
        return redirect(f'{settings.SUCCESSFUL_CODE_URL}')
    except EmailVerification.DoesNotExist:
        return Response({"error": "Invalid verification code."}, status=400)

# User registration
UserRegistrationView = UserRegistrationView.as_view()


# User login
UserLoginView = UserLoginView.as_view()


# Update and delete profile by user
UserUpdateProfileView = UserUpdateProfileView.as_view()


# Request password reset
RequestPasswordResetView = RequestPasswordResetView.as_view()


# Confirm password reset
PasswordResetConfirmView = PasswordResetConfirmView.as_view()


# Logout user
LogoutUser = LogoutUser.as_view()


# Set CSRF cookie
@ensure_csrf_cookie
def set_csrf_cookie(request):
    return JsonResponse({"message": "CSRF cookie set"})