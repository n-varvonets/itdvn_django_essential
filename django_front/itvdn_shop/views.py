import json
import random
import urllib.request

from django.views.generic import (TemplateView, ListView, DetailView, DateDetailView,
                                  WeekArchiveView, DeleteView, CreateView, UpdateView, FormView)
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User

from .forms import LoginForm, SignUpForm

url = urllib.request.urlopen("https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json")
words = json.loads(url.read())

# темплейты - инструмент, позволяющий добавлять логику, а наш фронтенд не используя js. Темплейт состоит из 4х конструкций: \
# переменные(выводять значения из контекста {{ }}), теги(добавляют логику {% %}), фильтры(преобразуют переменные. фильтры могут
# быть как в тегах {% if element|Length >4 %} то так и в переменных {{ element|Length }}), комментарии{# for example #}.
# Пару примеров фильтров: |Length, |upper, |Linebreaks, |filesizeformat, |join:"_TEST" - больше смотри в документации
# ВАЖНО ПОНИМАТЬ: темплейты используются-выполняются только на этапе рендеринга страницы, если нам необходимо делать какую-то
# логику на уже готовой странице - тогда используется js. Темплейт подойдет для тех проектов, где нет необходимости очень
# сложного фронт-енда. Т.е. для большого проекта используется js.


class Index(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        return {'some_data': [random.choice(words)
                              for i in range(10)]}


class Report(TemplateView):
    template_name = 'main/report.html'


class LoginExample(LoginView):
    pass


class ListExample(ListView):
    template_name = 'accounts/profile.html'
    queryset = User.objects.all()
    context_object_name = "users"


class DetailViewExample(DetailView):
    template_name = 'detail.html'
    model = User


class DateDetailViewExample(DateDetailView):
    template_name = 'date_detail.html'
    model = User
    date_field = "date_joined"


# Example http://127.0.0.1:8000/detail-date/2020/feb/24/2


class WeekArchiveViewExample(WeekArchiveView):
    template_name = 'week_archive.html'
    year = 2020
    model = User
    date_field = "date_joined"
    context_object_name = "week_users_archive"
#     http://127.0.0.1:8000/detail-date/2020/feb/24/2


class CreateViewExample(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = '/'


class UpdateExample(UpdateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = '/'


class DeleteExample(DeleteView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = '/'
