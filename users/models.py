from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.is_staff == True and self.is_superuser == True:
            self.is_active = True
            self.is_verified = True
        if self.is_verified and not self.is_active:
            self.is_active = True
        super().save(*args, **kwargs)


class EmailVerification(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    verification_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Email Verification'
        verbose_name_plural = 'Email Verifications'
