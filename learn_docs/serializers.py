from datetime import datetime

from rest_framework import serializers


class Comment:
    
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=20)
    created = serializers.DateTimeField()

    # если мы хотим сразу возвращать готовые обькты по валидированным данным данным
    def create(self, validated_data):
        print('created')
        # Comment.objects.create(**validated_data) ##  если хотим сразу в бд
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        print('update')
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.email)
        instance.created = validated_data.get('created', instance.email)
        # instance.save()
        return instance

    # # если нам не нужно создавать новый обьект, и например сделать какую нибудь логику(например, отправка сообщения на почту, можно переопределить save напрямую)
    # def save(self, **kwargs):
    #     email = self.validated_data.get('email')
    #     message = self.validated_data.get('message')
    #     # send_email(from=email, message=message)

    # для валидации поля мы создаем метод с названием validate_<field>
    # при неудачной валидации кидаем validation error
    # только для полей required true
    def validate_content(self, value):
        if 'django' not in value.lower():
            raise serializers.ValidationError('This comment is not about Django')
        return value

    # валидации на уровне обьекто
    def validate(self, attrs):
        # if attrs['start'] > attrs['finish']:
        #     raise serializers.ValidationError('finish ust occur after start')
        return attrs

    # можно написать валидатор, который будет использоваться для нескольких полей

    def multiple_of_ten(self, value):
        if value % 10 != 0:
            raise serializers.ValidationError('Not a muliply of ten')

    class GameRecord(serializers.Serializer):
        score = serializers.IntegerField(   )


