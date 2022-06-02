import graphene
from django.contrib.auth import get_user_model

from graphene_django import DjangoObjectType
from .models import Car, Make, Model


# дальше создаем наши типы из models. в graphql есть существующие типы (int, id, str), а мы здесь уже \
# создаем наши - кастомные(чем-то напоминает сериалиатор).
class MakeType(DjangoObjectType):
    """
    Указываем нашу модель с полями
    """
    class Meta:
        model = Make
        fields = ("id", "name")
        # можем добавить фильтры, т.е. искать не только по id, но еще по некоторым полям
        filter_fields = ('name', 'id')
        # {'name': ['exact', 'icontains', 'istartswith']}  - д возможность для фильтрации, будет искать гибкие записи,
        # которые начинаю с ... или имеют в себе
        interfaces = (graphene.relay.Node,)  #


class ModelType(DjangoObjectType):
    class Meta:
        model = Model
        fields = ("id", "name")


class CarType(DjangoObjectType):
    class Meta:
        model = Car
        fields = ("id", "license_plate", "make", "model")  # поле можно не указывать если хотим вывести все поля


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


