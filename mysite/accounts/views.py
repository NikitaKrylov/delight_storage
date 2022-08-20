from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from .forms import RegisterUserForm, AuthenticationUserForm
from .models import User


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterUserForm


class AuthenticationView(LoginView):
    form_class = AuthenticationUserForm
    template_name = 'accounts/authentication.html'


class UserProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        return HttpResponse("<h1>{}</h1>".format(user.username))
