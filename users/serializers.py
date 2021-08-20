from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import UserProfile, UserProfileContactInfo

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        # extra_kwargs = {'email': {'required': True}}
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=User.objects.all(),
        #         fields=('username', 'email')
        #     )
        # ]


    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    # def create(self, validated_data):
    #     return super().create(validated_data)

    # def create(self, validated_data):
    #     print(validated_data)
    #     return User.objects.create_user(**validated_data)

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


class UserProfileContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileContactInfo
        fields = ['website_link', 'twitter_link', 'github_link']


class UserProfileSerializer(serializers.ModelSerializer):
    contacts = UserProfileContactInfoSerializer(many=False, read_only=True) # так мы добавляем сериализованный обьект в другой обьект

    class Meta:
        model = UserProfile
        fields = ('logo', 'location', 'about', 'title', 'contacts')

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)



