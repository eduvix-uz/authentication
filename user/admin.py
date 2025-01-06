from django.contrib import admin
from .models import User, EmailVerification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'id')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    list_per_page = 30


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification_code', 'created_at', 'id')