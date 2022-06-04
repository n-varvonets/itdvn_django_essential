"""
ASGI config for LESSON_10 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
import os

import django
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websockets.settings')  # указываем env к файлу с переменными
django.setup()

application = ProtocolTypeRouter({  # подключаем наш роутер
    "http": AsgiHandler(),  # подключаем наш async обработчик
    "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    )),  # здесь мы указываем urls наших websockets , для этого в нашем приложении chat создаем два файла:
    # 1) consumers.py - обработчик наших websockets
    # 2) routing.py указываем грубо говоря url для нашего websock, нашего чата/комнаты. Работает это как обычные урл. Клиентский \
    # запрос попадает в urls, который перенаправляет запрос во вью. во вью если чат(id которого клиент передал в параметрах) то,
    # его комната берется с бд и возвращается или создается новая комната, после чего ответ возращается клие
})