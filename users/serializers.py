from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import UserProfile, UserProfileContactInfo

User = get_user_model()



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

class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    repeat_new_password = serializers.CharField()
    old_password = serializers.CharField()

    """ Здесь мы будем хранить логику по изменению пароля"""
    def save(self, **kwargs):
        user = kwargs.get('user')
        user.set_password(self.validated_data.get('new_password'))
        user.save()
        return user

    def validate(self, attrs):
        new_password = attrs.get('new_password')


    # def save(self, **kwargs):
    #     user = kwargs.get('user')
    #     print(user)
    #     old_password = kwargs.get('password')
    #     print(old_password)
    #     new_password = kwargs.get('new_password')
    #     user.set_password(new_password)
    #     user.save()

    # def validate_old_password(self, value: str) -> str:
    #     if value == self.old_password:
    #         raise serializers.ValidationError('Пароли совпадают')
    #     return super().validate_password(value)


class UserProfileContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileContactInfo
        fields = ['website_link', 'twitter_link', 'github_link']


class UserProfileSerializer(serializers.ModelSerializer):
    contacts = UserProfileContactInfoSerializer(many=False, read_only=True) # так мы добавляем сериализованный обьект в другой обьект

    class Meta:
        model = UserProfile
        fields = ('logo', 'location', 'about', 'title', 'contacts')

    # def create(self, validated_data):
    #     return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    user_profile = UserProfileSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'user_profile')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
        depth = 2
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

