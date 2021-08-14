from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import UserProfile

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email')
        # extra_kwargs = {'email': {'required': True}}
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=User.objects.all(),
        #         fields=('username', 'email')
        #     )
        # ]

    # def validate(self, data):
    #     print(data)
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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('id', )

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)



