from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
# Create your views here.
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import UserProfile
from users.permissions import IsResourceOwner
from users.serializers import CreateUserSerializer, UserProfileSerializer

User = get_user_model()

class GetUserAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )

    def get(self, request, *args, **kwargs):
        return Response('1')

## чтобы уж совсем не быть ленивым, я напишу свою регистрацию

class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    model = get_user_model()
    serializer_class = CreateUserSerializer

    ## этого можно было и не делать, но чисто для себя я написал
    def post(self, request, *args, **kwargs):
        print(request.user)
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TestClass(generics.RetrieveAPIView):
    multiple_lookup_fields = ('username', 'email', )
    # пример как сделать поиск по нескольким лукапам
    # данный метод вызывается тогда, когда достается обьект по лукапам
    # тут недоделанный вариант, пока нет в этом необходимости
    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.multiple_lookup_fields:
            filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

class UserProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    lookup_field = 'username'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsResourceOwner) ## данный пермиссионс требует авторизации только в тех методах запросов, которые изменяют данные
    authentication_classes = (JWTAuthentication, )
    serializer_class = UserProfileSerializer
    detail = {'detail': 'User with that id doesn\'t exist'}

    def get(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = self.serializer_class(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def patch(self, request, *args, **kwargs):
    #     return super().patch(request, *args, **kwargs)

    def get_object(self) -> UserProfile:
        user = User.objects.get(username=self.kwargs.get(self.lookup_field))  ## вот так достаем из lookup
        obj = get_object_or_404(self.get_queryset(), user=user)
        self.check_object_permissions(self.request, obj)
        return obj














