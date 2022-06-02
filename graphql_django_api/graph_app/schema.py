import graphene
from graphene_django import DjangoObjectType  # хотим создать типы для наших моделей и ниже импортируем наши модели:

from .models import Car, Make, Model

# дальше создаем наши типы из models. в grapgql есть суствующие типы (int, id, str), а мы здесь уже \
# создаем наши - кастомные(чем-то напоминает сериалиатор).
class MakeType(DjangoObjectType):
    """
    Указываем нашу модель с полями
    """
    class Meta:
        model = Make
        fields = ("id", "name")


class ModelType(DjangoObjectType):
    class Meta:
        model = Model
        fields = ("id", "name")


class CarType(DjangoObjectType):
    class Meta:
        model = Car
        fields = ("id", "license_plate", "make", "model")  # поле можно не указывать если хотим вывести все поля


class Query(graphene.ObjectType):
    """
    Создаим клас отором укажем наии возможности
    """
    # 1)создадим первый параметр из типа модели make
    make = graphene.Field(MakeType, id=graphene.Int())  # в котором в п передали наш тип модели и поле поиска - id с типом int

    # такое же и для машины
    car = graphene.Field(CarType, id=graphene.Int())
    model = graphene.Field(ModelType, id=graphene.Int())

    # 2)теперь настраиваем возможность вытянуть *все* типы
    makes = graphene.List(MakeType)
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


# 4) Подключаем к нашей главной схеме наш обьект Query. Можно так же мутации, но эт чуть позже
schema_my = graphene.Schema(query=Query)



