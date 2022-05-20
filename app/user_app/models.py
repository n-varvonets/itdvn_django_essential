from django.db import models

from django.contrib.auth.models import User
from user_app.managers import PersonManager


class Person(User):
    people = PersonManager()  # переименовываем нашего менеджера использвуя поля модели User

    class Meta:
        """
        proxy не изменяет контент пользователя, он только изменяет её поведение,
        т.е. без создания новой таблицы в бд + можно менять менеджер
        """
        proxy = True  # прокси не создает новую модель proxy=полномочие
        ordering = ('first_name',)   # если мы будем использовать класс Person, то по дефолту у нас будет сортировка по имени + \
        # ниже мы добавили новый метод, который будет только у данного класса(он не должен изменять данные о клиент в бд)

    def do_something(self):
        print(self.username)
