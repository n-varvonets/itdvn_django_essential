import os

from celery import Celery

# указываем дефолтное окружение
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_redis_rabbit.settings')

# создаем приложение
app = Celery('itvdn')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# + нужно указать наше приложение в inint.py
# celery -A celery_redis_rabbit worker -l DEBUG
# celery -A celery_redis_rabbit worker --beat --scheduler django --loglevel=debug  # для крона

