import json

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from notifications.models import Notification
from .forms import RegisterUserForm, AuthenticationUserForm, EditUserProfileForm, UserPasswordResetForm, \
    UserSetPasswordForm, UserSettingsForm
from .models import User, Subscription
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView
from posts.models import Post


class Signatory(View):
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
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


# --------------User Page---------------


class UserProfileView(LoginRequiredMixin, FormView):
    template_name = 'accounts/profile.html'
    login_url = reverse_lazy('login')
    form_class = EditUserProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        return context

    def get_form(self, form_class=None):
        user = self.request.user
        return EditUserProfileForm(initial={
            'username': user.username,
            'avatar': user.avatar,
            'email': user.email,
            'birth_date': user.birth_date
        })



@login_required(login_url=reverse_lazy('login'))
def edit_user_form(request, *args, **kwargs):
    ctx = {}
    form = EditUserProfileForm(request.POST, instance=request.user)

    ctx['has_changed'] = form.has_changed()
    if form.is_valid() and form.has_changed():
        form.save()
    return HttpResponse(json.dumps(ctx), content_type='application/json')


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    context_object_name = 'notifications'
    login_url = reverse_lazy('login')
    template_name = 'accounts/notifications.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list, **kwargs)
        context['title'] = 'Уведомления'
        return context

    def get_queryset(self):
        return self.model.objects.filter(recipient__id=self.request.user.id)


class SelfUserPostListView(LoginRequiredMixin, ListView):
    model = Post
    login_url = reverse_lazy('login')
    context_object_name = 'posts'
    template_name = 'accounts/self_user_posts.html'

    def get_queryset(self):
        return self.model.objects.filter(Q(status=0) & Q(author=self.request.user)).all()

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list, **kwargs)
        context['title'] = 'Посты пользователя'
        return context


class UserSettingsFormView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    form_class = UserSettingsForm
    template_name = 'accounts/settings.html'

    def get_form(self, form_class=None):
        return self.form_class(user=self.request.user)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list, **kwargs)
        context['title'] = 'Настройки'
        return context



