from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import CreateUserSerializer


class GetUserAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]

    def get(self, request, *args, **kwargs):
        return Response('1')

## чтобы уж совсем не быть ленивым, я напишу свою регистрацию

class CreateUserAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    model = get_user_model()
    serializer_class = CreateUserSerializer




