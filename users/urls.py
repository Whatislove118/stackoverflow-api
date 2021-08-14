from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import GetUserAPIView, CreateUserAPIView, CreateUserProfileAPIView

urlpatterns = [
    path('hello/', GetUserAPIView.as_view(), name='hello'),
    path('auth/', TokenObtainPairView.as_view(), name='auth'),
    path('refresh/', TokenRefreshView.as_view(), name='auth'),
    path('register/', CreateUserAPIView.as_view(), name='reg'),
    path('accounts/profile/', CreateUserProfileAPIView.as_view(), name='profile')
]