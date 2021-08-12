from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email']
        #extra_kwargs = {'email': {'required': True}}
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Event.objects.all(),
        #         fields=['room_number', 'date']
        #     )
        # ]

    # def validate(self, data):
    #     print(data)
    #     # тут можно написать свою валидацию
    #     return data
#
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         # Add custom claims
#         token['username'] = user.name
#         # ...
#         print(token)
#         return token


