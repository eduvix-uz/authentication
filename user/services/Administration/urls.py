from django.urls import path, include
from .Views.UpdateUser import UserManageViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'update-user', UserManageViewSet, basename='update-user')

urlpatterns = [
    path('', include(router.urls)),
]
