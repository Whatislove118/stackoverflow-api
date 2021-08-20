from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import GetUserAPIView, UserCreateAPIView, UserProfileDetailAPIView, TestClass

urlpatterns = [
    path('hello/', GetUserAPIView.as_view(), name='hello'),
    path('auth/', TokenObtainPairView.as_view(), name='auth'),
    path('refresh/', TokenRefreshView.as_view(), name='auth'),
    path('register/', UserCreateAPIView.as_view(), name='reg'),
    path('<str:username>/profile/', UserProfileDetailAPIView.as_view(), name='profile'),
    path('test/<str:u>/<str:p>/', TestClass.as_view()),
]