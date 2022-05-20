from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from phone_field import PhoneField


# Второй кастомный подход, когда нам необходимо прикреплять картинки/файлы к пользователям или другую доп.инфу.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # связь О2О к модели пользователя, что бы создать новую таблицу \
    # с наими данными и ползователь должен быть один.. т.к. нельзя добавить новые поля в User, то просто раширяем его модель добавляя картинки
    phone = PhoneField(blank=True, help_text='Contact phone number')
    birthday = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=150)
    photo = models.ImageField(upload_to='profile_pics')
    bio = models.TextField()

    def __str__(self):
        return self.user.username


# Реализован сигнал post_save модели User, т.е. когда у нас создается новый пользователь, новый инстанс модели User вызывает \
# метод модели post_save и вызывается наша функция update_profile_signal
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    """
    Если флажок created создан, то в таком случае мы создаем для него Profile
    sender - компонент, который посылает сигнал(новый пользователь модели User);
    receiver - наша функция(update_profile_signal), которая обрабатывает сигнал(создает профиль с o2o)
    """
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()


# AbstractBaseUser и AbstractUser самые сложные типы кастомизации модели пользователя(в отличии от proxy или наследования User
# со связью O2O) и нужно продумать наперед перед миграциями. Если есть возможность - необходимо их обходить.

# AbstractBaseUser нуно использовать, когда надо изменить аутентификацию пользователей, или когда нам не подходит стандартный
# процес работы с пользователями. Например, у стандартно процес логина использует имя и пароль, а мы хотим мыло и пароль..
# AbstractBaseUser - совершенно новая модель.(миграции + setting.py)

# AbstractUser - сабклас AbstractBaseUser и его полная версия. Т.е. AbstractBaseUser -> AbstractUser -> Наша_кастомная_модель.
# Её используют, когда нас устраивает аутентификация в джанго, но необходимо добавить доп инфу в модель User, но по каким-то
# причинам мы не хотим создавать доп. класс как в случае с proxy
