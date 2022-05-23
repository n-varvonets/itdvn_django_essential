from email.mime.image import MIMEImage

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import UserSignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.views.generic import TemplateView

from django.conf import settings
import os

#  для pip install mailchimp-marketing для подписки
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

# Пункты применения отправки писем:
# - 1)Информативные письма(обновление всем пользователям или отправка писем администратору при ошибках). Делел через gmail \
# и aws(через внутренний сервис simple_email_confirmation. минус этого что он платный, если хотим отправлять к неопозананным \
# пользователеям(тех что не указали в настройках aws, те что не ified by aws))
# - 2)Регистрация, а потом активация
# - 3)Оповещения покупателей(акции, сертификаты, промо и др.).т.е. для большого кол-ва пользователей сразу через mailchimp-marketing
# - 4)Сброс пароля; Уже джанго реализовал вью в django.contrib.auth ('reset_password_app.urls') для этого функционала, так что
# с точки зрения бека ничего нового использовать не нужно, только создавть ноый url звать и правильно назвать темлейты(_complite,
# _confirm, _done, _email, _form, _email, _subject.txt(тема письма)) и их переиспользовать. Но что бы мы не исользовали(любые
# внешние библиотеки) - принцип будет одним и тем же:
# - открывает нашу страницу
# - на странице ему необходимо ввести почту
# - он вводит почту и мы на почту ему отправляем ОДНОРАЗОВЫЙ линк с ключом(по кторому будем понимать что конкретно этот \
# пользователь хочет изменить мебе пароль)
# - меняет его и все!


class MyTestTemplateView(TemplateView):
    """1) Информативные письма(обновление всем пользователям или отправка писем администратору при ошибках) """

    template_name = 'hello_email.html'

    # 1)пример обычного текста(минус данного подхода через send_mail заключается в том что картинки емейле не отображается)
    # def get(self, request):
        # 1)пример обычного текста(минус данного подхода через send_mail заключается в том что css в емейле не отображается)
        # send_mail('Some subject of mail', 'some main text', 'from@gmail.com',
        #           ['bolageg975@cupbest.com'], fail_silently=True)  # когда откроется страница, то нам отправится сообщение, \
        # fail_silently=True т.е. если где-то что-то пойдет не так при отправке письма, то это не будет прерывать работу сервера

        # 2) пример с генерацией html страницы, к примеру нашего темплейта
        # html_message = render_to_string(self.template_name)  # если надо, то можем передать вторым параметром контекст
        # send_mail('Some subject of mail', 'Hello my client', 'nickolay.varvonets@gmail.com',
        #           ['bolageg975@cupbest.com'], html_message=html_message)
        # return render(request, self.template_name)

    # 2) Пример с отображением css в емейле при помощи:
    #   - приложения в settings 'django_inlinecss',
    #   -  темплейте {% load inlinecss %}, {% inlinecss "css/email.css" %}, {% endinlinecss %}
    #   - и двух функций logo_data(),MIMEmage  и  get() EmailMultiAlternative
    def logo_data(self, image_name):
        print(f'image_name = {image_name}')
        with open(os.path.join(settings.MEDIA_ROOT, image_name), 'rb') as f:  # перносим из файла в бит
            log_data = f.read()

        # добавляем в наше сообщение с добавлением header
        logo = MIMEImage(log_data)
        logo.add_header('Content-ID', f'<{image_name}>')
        logo.add_header('Content-Disposition', 'inline', filename=image_name)
        return logo

    def get(self, request):
        html_message = render_to_string(self.template_name)  # если надо, то можем передать вторым параметром контекст

        email_message = EmailMultiAlternatives(
            subject='Some title lik "Happy day of victory"',
            body='some context like ptn pnh!',
            from_email='from@mail.com',
            to=['bolageg975@cupbest.com']
        )
        email_message.attach_alternative(html_message, 'text/html')
        email_message.mixed_subtype = 'related'

        # клюевой ньюанс подключения медиа файлов:
        for image in os.listdir(settings.MEDIA_ROOT):  # берем нашу картинку и переводим из файлов в бит формат
            email_message.attach(self.logo_data(image))  # добавляем уже битовую картинку к нашему сообщению
        email_message.send(fail_silently=False)

        return render(request, self.template_name)


"""2.1)Регистрация, а потом активация"""
def usersignup(request):
    """форма для регистрации где созлдаем пользователя, но НЕАКТИВНОГО(user.is_active = False)"""
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)   # но форму не сохраняем при след её вызове GET
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            # создаем письмо с генерацией токена
            email_subject = 'Activate Your Account'
            message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            # отправляем письмо
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse(
                'We have sent you an email, please confirm your email address to complete registration')
    else:
        form = UserSignUpForm()
    return render(request, 'signup.html', {'form': form})


def activate_account(request, uidb64, token):
    """
    когда в письме юзер переходит по линку, то он попадает сюда,
    где активируем нашего пользователя и сохраняем в бд
    """
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')


# https://us11.admin.mailchimp.com/account/add-api-key/ - даем апи кей
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID


"""3)Оповещения покупателей(акции, сертификаты, промо и др.).т.е. для большого кол-ва пользователей сразу через mailchimp-marketing"""
# Subscription Logic
def subscribe(email):
    """
     Contains code handling the communication to the mailchimp api
     to create a contact/member in an audience/list.
    """

    # назначаем сервер
    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    # добавляем пользователя,который подписался
    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))


def subscription(request):
    """
    получаем данные с фронта и записываем их
    :param request:
    :return:
    """
    if request.method == "POST":
        email = request.POST['email']
        print(email)
        subscribe(email)
        messages.success(request, "Email received. thank You! ")

    return render(request, "subscription.html")
