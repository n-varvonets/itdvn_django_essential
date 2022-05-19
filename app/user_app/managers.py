from django.db import models


class PersonManager(models.Manager):
    """
    Менеджер - интерфейс, через который создаются запросы к бд, который нужно в модели переименовать.
    Служат для того что бы добавлять доп. методы в модель или же изменять базовые вытягиваняия из модели, т.е. изменять
    базовый queryset
    """

    def get_staff_users(self):
        """
        :return: тех пользователей у который стаф == тру, т.е. наших сотрудников и админитраторов
        """
        return super(PersonManager, self).get_queryset().filter(is_staff=True)
