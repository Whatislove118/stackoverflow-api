import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, permissions, status, viewsets

# Create your views here.
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from learn_docs.mixins import MultipleFieldLookupMixin
from learn_docs.serializers import Comment, CommentSerializer
from users.serializers import UserProfileSerializer, UserSerializer

User = get_user_model()

# добавляем миксин и все ок в целом

class TestSerializers(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    authentication_classes = (JWTAuthentication, )

    def get(self, request, *args, **kwargs):
        comment = Comment(email='leila@example.com', content='foo bar')
        # serializing
        serializer = self.get_serializer(comment)
        print(serializer.data) # здесь мы транслируем лишь в нативный питоновский словарь. Нужны рендеры
        # json = JSONRenderer().render(serializer.data)
        # print(json)
        return Response(serializer.data)  ## рендер вызывается автоматически

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) ## нужно указывать дата
        comment = None
        if serializer.is_valid(raise_exception=True):
            comment = serializer.save() # create
            # comment = serializer.save(owner=request.user) # можно добавлять информацию при save, которая не находится в request.data
        ## вызов create или update в методе save зависит от того, как мы обьявили сериализатор
        # print(comment)
        # serializer = self.get_serializer(data=request.data, instance=comment)
        # if serializer.is_valid():
        #     comment = serializer.save() # update
        # print(comment)
        return Response(serializer.validated_data)

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         self.permission_classes = (AllowAny,)
    #     else:
    #         self.permission_classes = (IsAuthenticated, )
    #     return super().get_permissions()

    # def get_serializer(self, *args, **kwargs):
    #     if self.request.method == 'GET':
    #         self.serializer_class = CommentSerializer
    #     else:
    #         self.serializer_class = UserSerializer
    #     return super().get_serializer(*args, **kwargs)


class TestList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True) ## флаг того, что много инстансов
        return Response(serializer.data)

class TestRequestAPIView(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    authentication_classes = (JWTAuthentication, )
    lookup_fields = ('id', 'username', )

    def get(self, request, *args, **kwargs):
        print(request.query_params)
        return Response('1', status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset() ## очень важно вызывать данный метод, чем обращаться к проперте напрямую, тк при обращении напрямую, он кэшируется и получается грустно невкусно
        print(request.data)
        print(request.accepted_renderer)
        print(request.user)
        print(request.auth) # тут крч содержится токен(или может что то другое), что является параметром для аутентификации
        response = Response()
        request.data['1'] = '2'
        print(response.set_cookie('COKA', '12345', max_age=5))
        return response

    def handle_exception(self, exc): # вот так можно хэндлить ошибки любые(даже ерроры)(мб и не все)
        print(type(exc))
        return Response(data={'detail': 'pizda', })

    #def filter_queryset(self, queryset): фильтрует queryset (там нужны фильтры бэкэнды)

    # если нужно определить гибко сериализоатор, то как вариант. Если переопределяем, обращаемся только через метод(да и вообще всегда)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return UserProfileSerializer
        return UserSerializer

    # хуки
    # нужны для того, чтобы можно было переопределить сохранение или удаление внутри миксина(CreateModelMixin и тд вызывают их)

    # в данном случае очень удобно добавлять при сохранении информацию, которая передается вместе с request, но не с request.data
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # в данном случае можно вставлять определенную логику до или после сохранение
    def perform_update(self, serializer):
        #logger.log('update instance')
        instance = serializer.save() ## сохранение изменненных данных
        ##send_email_confirmation(user=self.request.user, modified=instance)

    ## также можно внедрять валидацию
    # def perform_create(self, serializer):
    #     queryset = SignupRequest.objects.filter(user=self.request.user)
    #     if queryset.exists():
    #         raise ValidationError('You have already signed up')
    #     serializer.save(user=self.request.user)


# если придется часто использовать данный миксин, можно создать базовый класс
class BaseRetrieveView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    pass

class BaseRetrieveUpdateDestroyView(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    pass

### тесты классов
### В целом если мы переопределяем поведения методов, то настраивать некоторые параметры необязательно(если они нам в коде не нужны)
## но в целом тенденция такая, что для retrieve нам нужен полюбому queryset и model
### для create,update достаточно модели (и для delete тоже), однако в целом, иногда очень полезно вызывать queryset в коде через класс представления, а не через модель напрямую(например ели queryset отфильтрован)



## view set
## обычный класс - не содежит действий
## GenericViewSet добавляет стандартную логику для вьюшек(действий также не содержит)
## ReadOnlyViewSet - list() и retrieve()
## ModelViewSet - содержит все методы(использовать можно, но для себя в крайне редких случаях)
## для всех них (кроме ModelViewSet) удобно использовать роутер
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication, )
    ## так мы можем устанавливать permissions для конкретного юрл

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (AllowAny, )
        return (permission() for permission in permission_classes)

    # благодаря данному декоратору можем создавать свои action. Можно настроить хоть пермиссион хоть что
    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    # def list(self, request, *args, **kwargs):
    #     queryset = User.objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)

    # у вью сета нету методов хендлеров вроде get post и тд



