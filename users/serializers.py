from rest_framework import serializers
from .models import User
from .utils import send_verification_email
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.contrib.auth import authenticate
from django.conf import settings


# User registration
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'photo', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        send_verification_email(user) 
        return user
    

# User login
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        # Return only relevant user details
        return {"username": user.username, "id": user.id, "is_staff": user.is_staff}


# User profile read, update and delete
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'photo', 'is_active', 'is_verified', 'id')

    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.is_verified = validated_data.get('is_verified', instance.is_verified)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance
    

# Request reset password
class RequestPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user is associated with this email.")
        return value

    def save(self, request):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        reset_url = f"{settings.FRONTEND_DOMAIN_NAME}/change-password?uidb64={uid}&token={token}"
        send_mail(
            subject="prohub.uz shaxsiy kabinet parolini tiklash so'rovi",
            message=f"Quyidagi havolaga kirish orqali shaxsingizni tasdiqlang: {reset_url}",
            from_email=f'{settings.EMAIL_HOST_USER}',
            recipient_list=[email],
        )


# Reset password
class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uidb64']))
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid UID")

        if not PasswordResetTokenGenerator().check_token(self.user, data['token']):
            raise serializers.ValidationError("Invalid or expired token")

        return data

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()
        send_mail(
            subject=f"Parol o'zgartirildi",
            message=f"{settings.FRONTEND_DOMAIN_NAME} platformadagi parolingiz muvaffaqiyatli o'zgartirildi.\n\n"
                    f" Yangi parolingiz: {self.validated_data['new_password']}, Loginingiz: {self.user.username}",
            from_email=f'{settings.EMAIL_HOST_USER}',
            recipient_list=[self.user.email],
        )


# View user details
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_active', 'is_verified', 'id', 'first_name', 'last_name')


# Logout user
class LogoutUserSerializer(serializers.Serializer):
    pass