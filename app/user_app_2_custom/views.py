from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.views.generic import FormView, UpdateView
# from .models import Person
from django.contrib.auth.models import User

from .forms import SignUpForm, ProfileForm
from .models import Profile


class Index(TemplateView):
    template_name = 'index.html'


class CreatUser(FormView):
    form_class = UserCreationForm  # джанго предоставляеть
    template_name = 'signup2.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(CreatUser, self).form_valid(form)


class UpdateProfile(UpdateView):
    """Новая модель где будем добавлять к нашему пользователю картинки-файлы, телефон и дату рождения"""
    model = Profile
    form_class = ProfileForm
    template_name = 'user_profile.html'
    success_url = '/'

    def form_valid(self, form):
        user = self.request.user
        user.profile.phone = form.cleaned_data.get('phone')
        user.profile.birthday = form.cleaned_data.get('birthday')
        if 'photo' in self.request.FILES:  # если в нашем риквесте был передан аттр 'photo'
            print('found it')
            user.profile.photo = self.request.FILES['photo']

        print(self.request.FILES)
        print(user.profile.photo)
        user.save()
        return super(UpdateProfile, self).form_valid(form)


class AllUsers(TemplateView):
    template_name = "all_users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['users'] = Person.people.get_staff_users()  # применим наш созданный метод в новом менеджере
        # context['users'] = User.objects.filter(is_staff=True)   # у objects даже нет такого метода, но можно это можно \
        # и так выбрать наш стафф
        return context