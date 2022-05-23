from django.contrib import admin
from django.urls import path, include

from .views import MyTestTemplateView , usersignup, activate_account, subscription
from django.contrib.auth import views as auth

urlpatterns = [
    path('test-email/', MyTestTemplateView.as_view(), name='test-email'),

    #
    # path('logout/', auth.LogoutView.as_view(template_name='index.html'), name='logout'),
    path(r'signup/', usersignup, name='register_user'),  # url для регистрационной формы, после чего отправляем письмо
    path(r'activate/<uidb64>/<token>/', activate_account, name='activate'),  # в письме при регистрации приходит этот линк

    path("subscription/", subscription, name="subscription"),  # url для подписки
]
