from django.core.mail import send_mail
from django.conf import settings
from .models import EmailVerification


def send_verification_email(user):
    verification_record, created = EmailVerification.objects.get_or_create(user=user)
    
    # Email content
    subject = 'Elektron pochtani tasdiqlash'
    verification_url = f"{settings.SERVER_NAME}/profile/verify-email/{verification_record.verification_code}/"
    message = f"Salom {user.first_name} {user.last_name},\n\nQuyidagi havola orqali elektron pochtangizni tasdiqlang:\n\n{verification_url}\n\nRaxmat!"
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    print("Email sent successfully.")
