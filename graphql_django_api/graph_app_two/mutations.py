import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import create_refresh_token, get_token

from graph_app.types import MakeType  #, UserType
from graph_app.models import Make


# Используем InputObjectType для создания наших мутаций
class MakeInput(graphene.InputObjectType):
    # указываем те поля, которые пользователь будет вводить
    id = graphene.ID()
    name = graphene.String()


class CreateMake(graphene.Mutation):
    # создаем класс для создания нашего производителя CreateMake
    class Arguments:
        input = MakeInput(required=True)  # input тот, который мы создали выше, без required=True нам не будет ничего изменять

    ok = graphene.Boolean()  # есть такая практика
    make = graphene.Field(MakeType)  # и в наше поле имортируем наш тип модели

    # @staticmethod
    # def mutate(self, info, input=None):
    #     """создаем собсна функцию, которая будет делать создание наших обьектов"""
    #     ok = True
    #     make_instance = Make.objects.create(name=input.name)
    #     return CreateMake(ok=ok, make=make_instance)

    @classmethod
    def mutate(cls, root, info, input=None):
        """создаем собсна функцию, которая будет делать создание наших обьектов"""
        print('-------------777', input)
        ok = True
        make_instance = Make.objects.create(name=input.name)
        return cls(ok=ok, make=make_instance)  # что бы пользователь могу увидеть что создал, мы возвращаем ему эти данные


class UpdateMake(graphene.Mutation):

    class Arguments:
        id = graphene.Int(required=True)
        input = MakeInput(required=True)

    ok = graphene.Boolean()
    make = graphene.Field(MakeType)

    @classmethod
    def mutate(cls, info, id, input=None):
        ok = False
        try:
            # пробуем получить наш обьект
            make_instance = Make.objects.get(pk=id)
        except Make.DoesNotExist:
            return cls(ok=ok, make=None)

        ok = True
        make_instance.name = input.name  # изменяем наш аттрибут и сохраняем
        make_instance.save()
        return cls(ok=ok, make=make_instance)


class DeleteMake(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            make_instance = Make.objects.get(pk=id)
            make_instance.delete()
            return cls(ok=True)
        except Make.DoesNotExist:
            return cls(ok=True)

#
# class CreateUser(graphene.Mutation):
#     user = graphene.Field(UserType)
#     token = graphene.String()
#     refresh_token = graphene.String()
#
#     class Arguments:
#         password = graphene.String(required=True)
#         email = graphene.String(required=True)
#
#     def mutate(self, info, password, email):
#         user = get_user_model()(
#             email=email,
#         )
#         user.set_password(password)
#         user.save()
#
#         token = get_token(user)
#         refresh_token = create_refresh_token(user)
#
#         return CreateUser(user=user, token=token, refresh_token=refresh_token)


class Mutation(graphene.ObjectType):
    # наш класс мутаций в которую мы будем передавать в общую схему
    create_make = CreateMake.Field()
    update_make = UpdateMake.Field()
    delete_make = DeleteMake.Field()
    # create_user = CreateUser.Field()
