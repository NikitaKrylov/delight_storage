import json
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from .models import Notification
from .forms import RegisterUserForm, AuthenticationUserForm, EditUserProfileForm, UserPasswordResetForm, \
    UserSetPasswordForm, UserSettingsForm
from .models import User, Subscription
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView
from posts.models import Post, PostDelay
from mediacore.forms import ImageFileFormSet
from posts.forms import CreatePostDelayForm, PostForm


class Signatory(View):
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
        ctx = {"has_sub": None}
        user: User = request.user
        if user.is_authenticated:
            # подписка уже имеется
            if user.subscriptions.filter(subscription_object__id=kwargs['object_id']).exists():
                user.subscriptions.filter(
                    subscription_object__id=kwargs['object_id']).delete()  # больше нету
                ctx["has_sub"] = False
            else:
                sub = Subscription(
                    subscription_object=User.objects.get(
                        id=kwargs['object_id']),
                    subscriber=user
                )
                sub.save()
                user.subscriptions.add(sub)
                ctx["has_sub"] = True

        return HttpResponse(json.dumps(ctx), content_type='application/json')


# --------Authentivation / Register-------


def logout_view(request):
    logout(request)
    return redirect('post_list')


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('post_list')


class AuthenticationView(LoginView):
    form_class = AuthenticationUserForm
    template_name = 'accounts/authentication.html'
    success_url = reverse_lazy('post_list')


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


class UserNotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    context_object_name = 'notifications'
    login_url = reverse_lazy('login')
    template_name = 'accounts/notifications.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Уведомления'
        return context

    def get_queryset(self):
        return self.model.objects.filter(recipient__id=self.request.user.id)


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    login_url = reverse_lazy('login')
    context_object_name = 'posts'
    template_name = 'accounts/self_user_posts.html'

    def get_queryset(self):
        return self.model.objects.filter(Q(status=0) & Q(author=self.request.user)).all()

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Посты пользователя'
        return context


class UserSettingsFormView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    form_class = UserSettingsForm
    template_name = 'accounts/settings.html'

    def get_form(self, form_class=None):
        return self.form_class(user=self.request.user)

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Настройки'
        return context


@login_required(login_url=reverse_lazy('login'))
def edit_user_settings(request, *args, **kwargs):
    ctx = {}
    form = UserSettingsForm(request.POST, user=request.user)

    if form.is_valid():
        pass

    return HttpResponse(json.dumps(ctx), content_type='application/json')


class UserSubscriptionListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'accounts/subscriptions.html'
    model = Subscription
    context_object_name = 'subscriptions'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Подписки'
        return context

    def get_queryset(self):
        return Subscription.objects.filter(subscriber=self.request.user).all()


class CreatePostView(LoginRequiredMixin, CreateView):

    login_url = reverse_lazy('login')
    template_name = 'accounts/post_add.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать пост'
        context['image_formset'] = ImageFileFormSet()
        context['delay_form'] = CreatePostDelayForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST)
        image_formset = ImageFileFormSet(
            request.POST, request.FILES, instance=form.instance)
        delay_form = CreatePostDelayForm(request.POST)

        if form.is_valid() and image_formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            if delay_form.is_valid():
                delay = delay_form.save()
                post.delay = delay
                post.save()

            images = image_formset.save(commit=False)
            for image in images:
                image.save()

            return redirect(reverse('change_post', kwargs={'pk': post.pk}))

        return render(request, self.template_name, {'form': form, 'image_formset': image_formset, 'delay_form': delay_form})


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    login_url = reverse_lazy('login')
    template_name = 'accounts/post_change.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование'

        post = self.get_object()
        context['post'] = post
        context['image_formset'] = ImageFileFormSet(instance=post)
        context['delay_form'] = CreatePostDelayForm(
            instance=post.delay or None)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST, instance=self.get_object())

        if form.is_valid():
            post = form.save()

            delay_form = CreatePostDelayForm(
                request.POST, instance=post.delay or None)
            if delay_form.is_valid():
                delay = delay_form.save()
            else:
                delay_form = CreatePostDelayForm()
                if post.delay:
                    post.delay.delete()
                    post.delay = None
                    if post.status == 1:
                        post.status = 0
                    post.save()

            image_formset = ImageFileFormSet(
                request.POST, request.FILES, instance=post)
            images = image_formset.save()

        else:
            delay_form = CreatePostDelayForm()

        return render(request, self.template_name, {'form': form, 'delay_form': delay_form, 'image_formset': ImageFileFormSet(instance=form.instance)})

    def get_form(self, *args, **kwargs):
        return self.get_form_class()(instance=self.object)

# class LikedPostList(PostQueryMixin, PostFilterFormMixin, ListView):
#     model = Post
#     paginate_by = 30
#     template_name = 'posts/images.html'
#     context_object_name = 'posts'

#     def get_queryset(self):
#         return super().get_queryset().filter(likes__user=self.request.user)
