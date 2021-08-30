from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import TestRequestAPIView, TestList, UserViewSet, TestSerializers

## 1 вариант
urlpatterns = [
    path('request/', TestRequestAPIView.as_view()),
    path('list/', TestList.as_view()),
    path('user/', UserViewSet.as_view({'get': 'list'})),
    path('user/<uuid:pk>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('serializer/', TestSerializers.as_view())




]
## тк юрл самому писать тяжело и запарно, необходим роутер
## 2 вариант для вьюсетов
router = DefaultRouter()
router.register(r'user-set', UserViewSet, basename='user')
urlpatterns += router.urls
