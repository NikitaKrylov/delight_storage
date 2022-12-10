import json

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from notifications.models import Notification
from .forms import RegisterUserForm, AuthenticationUserForm, EditUserProfileForm, UserPasswordResetForm, \
    UserSetPasswordForm
from .models import User, Subscription
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView


class Signatory(View):
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
        print(1312312312312313)
        ctx = {"has_sub": None}
        user: User = request.user
        if user.is_authenticated:
            if user.subscriptions.filter(subscription_object__id=kwargs['object_id']).exists(): # подписка уже имеется
                user.subscriptions.filter(subscription_object__id=kwargs['object_id']).delete() # больше нету
                ctx["has_sub"] = False
            else:
                sub = Subscription(
                        subscription_object=User.objects.get(id=kwargs['object_id']),
                        subscriber=user
                    )
                sub.save()
                user.subscriptions.add(sub)
                ctx["has_sub"] = True

        return HttpResponse(json.dumps(ctx), content_type='application/json')


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


# --------------User---------------


class UserProfileView(LoginRequiredMixin, UpdateView):
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
