from django.db import models
from django.contrib.auth.models import AbstractUser

from graph_app.managers import UserManager


class ApiClient(AbstractUser):
    username = None  # де ло кто использует ник - чаще всего мыло
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = 'email'  # место нашего USERNAME_FIELD будет наше поле 'email
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_username(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "API client"
        verbose_name_plural = "API clients"

    def __str__(self):
        return f"{self.pk}_{self.email}"


class Make(models.Model):
    """производитель машины"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Model(models.Model):
    """марка машины"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Car(models.Model):
    """
    сама машина:
        - у машины может быть несколько производителей - (разные машины могут иметь одного и того же производителя.?)

    """
    license_plate = models.CharField(unique=True, max_length=10)
    notes = models.TextField()
    make = models.ForeignKey(
        Make, related_name="car_make", on_delete=models.CASCADE
    )

    model = models.ForeignKey(
        Model, related_name="car_model", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.license_plate}_{self.make.name}_{self.model.name}"
