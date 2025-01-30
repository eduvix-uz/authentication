from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from users.permissions import IsAdminPermission

schema_view = get_schema_view(
    openapi.Info(
        title = "prohub.uz Authentication service API",
        default_version="v1",
        description="This is a documentation for prohub.uz authentication service API",
        contact=openapi.Contact("dilshod.normurodov1392@gmail.com", "dil-shod.uz"),
    ),
    public=True,
    permission_classes=[permissions.IsAuthenticatedOrReadOnly,],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include('users.urls')),
    path('manager/', include('users.services.Administration.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    path('docs/', schema_view.with_ui('swagger',cache_timeout=0),name='swagger-docs'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),