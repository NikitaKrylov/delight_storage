from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from notifications.models import Notification
from .forms import RegisterUserForm, AuthenticationUserForm, EditUserProfileForm, UserPasswordResetForm, \
    UserSetPasswordForm
from .models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView


#--------Authentivation / Register-------


def logout_view(request):
    logout(request)
    return redirect('post_list')


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterUserForm


class AuthenticationView(LoginView):
    form_class = AuthenticationUserForm
    template_name = 'accounts/authentication.html'


# --------------User---------------

class UserProfileView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile.html'
    model = User
    context_object_name = 'user'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.username
        return context


class EditUserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile_edit.html'
    form_class = EditUserProfileForm
    model = User
    success_url = reverse_lazy('profile')
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.username
        return context

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    context_object_name = 'notifications'
    login_url = reverse_lazy('login')
    template_name = 'accounts/notifications.html'

    def get_queryset(self):
        return self.model.objects.filter(recipient__id=self.request.user.id)


# -----------------------Password reset-----------------------------

class UserPasswordResetView(PasswordResetView):
    """1. Ввод почты для отправки письма с инструкциями"""
    template_name = 'accounts/password_reset/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    form_class = UserPasswordResetForm
    email_template_name = 'accounts/password_reset/password_reset_email.txt'


class UserPasswordResetDoneView(PasswordResetDoneView):
    """2. Сообщение об отправке письма на почту"""
    template_name = 'accounts/password_reset/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """3. Поле для ввода нового пароля"""
    template_name = 'accounts/password_reset/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    form_class = UserSetPasswordForm


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    """4. Уведомление об успешном изменении пароля"""
    template_name = 'accounts/password_reset/password_reset_complete.html'

