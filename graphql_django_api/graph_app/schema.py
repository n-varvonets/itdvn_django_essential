import graphene
from graphene_django.filter import DjangoFilterConnectionField

# дальше создаем наши типы из models. в graphql есть существующие типы (int, id, str), а мы здесь уже \
# создаем наши - кастомные(чем-то напоминает сериалиатор).
# импортируем созданные и перенесенные в types ноши кастомные типы
from django.contrib.auth import get_user_model
from .types import CarType, MakeType, ModelType, UserType
from .models import Car, Make, Model


class Query(graphene.ObjectType):
    """
    Создадим клас отором укажем наии возможности
    """
    # 1)создадим первый параметр из типа модели make
    # make = graphene.Field(MakeType, id=graphene.Int())  # в котором в п передали наш тип модели и поле поиска - id с типом int

    # 1.1) случай когда мы хотим добавим доп поля для поиска(фильтрации) к примеру не только по id, но и по name
    make = graphene.relay.Node.Field(MakeType)  # в котором в п передали наш тип модели и поле поиска - id с типом int
    makes = DjangoFilterConnectionField(MakeType)  # для множества елементов фильтр

    # такое же и для машины
    car = graphene.Field(CarType, id=graphene.Int())
    model = graphene.Field(ModelType, id=graphene.Int())

    # 2)теперь настраиваем возможность вытянуть *все* типы
    # makes = graphene.List(MakeType)  # чий варик, но выше добавим возможность с доп полем писка(фильтра)
    cars = graphene.List(CarType)
    models = graphene.List(ModelType)

    # 3) добавим распознаватели(resolves)
    def resolve_make(self, info, **kwargs):

        # из наших kwargs вытягиваем id
        id = kwargs.get('id', None)  # ВАЖНО: Саня get с дикта и по дефолту вторым параметром

        # если есть, то возвращаем нашего производителя или же ничего
        try:
            return Make.objects.get(id=id)
        except Make.DoesNotExist:
            return None

    def resolve_car(self, info, **kwargs):
        id = kwargs.get('id', None)

        try:
            return Car.objects.get(id=id)
        except Car.DoesNotExist:
            return None

    def resolve_makes(self, info, **kwargs):
        try:
            return Make.objects.all()
        except Make.DoesNotExist:
            return None

    def resolve_cars(self, info, **kwargs):
        try:
            return Car.objects.all()
        except Car.DoesNotExist:
            return None

    def resolve_model(self, info, **kwargs):
        id = kwargs.get('id', None)

        try:
            return Model.objects.get(id=id)
        except Model.DoesNotExist:
            return None

    def resolve_models(self, info, **kwargs):
        try:
            return Model.objects.all()
        except Model.DoesNotExist:
            return None

    # тоже самое проделываем и для нашего пользотваля, но
    api_client = graphene.Field(UserType)
    api_clients = graphene.List(UserType)

    def resolve_api_client(self, info):
        user = info.context.user
        # здесь провемя пользотвателя наш - ананимус?
        if user.is_anonymous:
            raise Exception('Authentication Failure: Your must be signed in')
        return user

    def resolve_api_clients(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('Authentication Failure: Your must be signed in')
        if not user.is_staff:
            raise Exception('Authentication Failure: Must be Manager')
        return get_user_model().objects.all()


# 4) Подключаем к нашей главной схеме наш обьект Query. Можно так же мутации, но эт чуть позже
# schema_my = graphene.Schema(query=Query)
#  так делают если не импортируют текущий файл в главный нашего приложения(graphql_django_api)


