import requests
from celery import shared_task

from celery_redis_rabbit.celery import app

print('app---', app)

@app.task
def fibon(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b,
    return a


@shared_task  # типо крона - запускается раз в n чего-то с помощи активации в settings аттрибута CELERY_BEAT_SCHEDULE
def fetch_weather():

    """используя апи получаем скорость ветра в городе"""
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=5b9dee532cf418833e63baf01e31e197'
    city = 'Las Vegas'
    city_weather = requests.get(url.format(
        city)).json()
    return city_weather.get('wind')
# celery -A celery_redis_rabbit worker --beat --scheduler django --loglevel=debug
