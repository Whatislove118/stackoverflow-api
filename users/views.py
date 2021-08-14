from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, status
# Create your views here.
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import UserProfile
from users.serializers import CreateUserSerializer


class GetUserAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [JWTAuthentication, ]

    def get(self, request, *args, **kwargs):
        return Response('1')

## чтобы уж совсем не быть ленивым, я напишу свою регистрацию

class CreateUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    model = get_user_model()
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class CreateUserProfileAPIView(generics.CreateAPIView):
#     permission_classes = (IsAuthenticated, )
#     model = UserProfile
#     serializer_class = ...








