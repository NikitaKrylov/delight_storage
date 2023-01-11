import datetime
import json
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Variance, Count, F
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView

from .mixins import CheckUserConformity
from .models import Notification
from .forms import RegisterUserForm, AuthenticationUserForm, EditUserProfileForm, UserPasswordResetForm, \
    UserSetPasswordForm, UserSettingsForm
from .models import User, Subscription
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView
from posts.models import Post, PostDelay
from mediacore.forms import ImageFileFormSet
from posts.forms import CreatePostDelayForm, PostForm
from django.contrib.auth import login, authenticate

from posts.models import Like

from posts.mixins import AnnotateUserLikesMixin


class SignatoryView(View):
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

    def form_valid(self, form):
        _redirect = super().form_valid(form)
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        if user is not None and user.is_active:
            login(self.request, user, backend='mysite.backends.AuthBackend')
            return _redirect
        return render(self.request, self.template_name, content={'form': form})


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

    def post(self, request, *args, **kwargs):
        form = EditUserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('profile')


@login_required(login_url=reverse_lazy('login'))
def edit_user_form(request, *args, **kwargs):
    ctx = {}
    form = EditUserProfileForm(request.POST, request.FILES, instance=request.user)

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
        user = self.request.user
        context['unread'] = user.notifications.filter(unread=True, deleted=False)
        context['readed'] = user.notifications.filter(unread=False, deleted=False)
        return context

    def get_queryset(self):
        return self.model.objects.filter(recipient__id=self.request.user.id)


@login_required(login_url=reverse_lazy('login'))
def delete_notification(request, *args, **kwargs):
    notification = Notification.objects.get(pk=kwargs['pk'])

    if request.user != notification.recipient:
        raise PermissionDenied()

    notification.deleted = True
    notification.unread = False
    notification.save()
    return redirect('user_notifications')


@login_required(login_url=reverse_lazy('login'))
def read_notification(request, *args, **kwargs):
    notification = Notification.objects.get(pk=kwargs['pk'])

    if request.user != notification.recipient:
        raise PermissionDenied()

    notification.unread = False
    notification.save()
    return redirect('user_notifications')


@login_required(login_url=reverse_lazy('login'))
def delete_all_notification(request, *args, **kwargs):
    request.user.notifications.update(deleted=True, unread=False)
    return redirect('user_notifications')


@login_required(login_url=reverse_lazy('login'))
def read_all_notification(request, *args, **kwargs):
    request.user.notifications.update(unread=False)
    return redirect('user_notifications')


class UserPostListView(LoginRequiredMixin, ListView, AnnotateUserLikesMixin):
    model = Post
    login_url = reverse_lazy('login')
    context_object_name = 'posts'
    template_name = 'accounts/self_user_posts.html'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user).all()

    def get_context_data(self, *args, object_list=None, **kwargs):
        user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Мои посты'
        context['likes_amount'] = Post.objects.count_field_elements('likes', user)
        context['views_amount'] = Post.objects.count_field_elements('views', user)
        context['comments_amount'] = Post.objects.count_field_elements('comments', user)
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
        return self.model.objects.filter(subscriber=self.request.user).all()

# ------------------------- Posts ----------------------------


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
        image_formset = ImageFileFormSet(request.POST, request.FILES, instance=form.instance)
        delay_form = CreatePostDelayForm(request.POST)

        if form.is_valid() and image_formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            if delay_form.is_valid():
                delay = delay_form.save()
                post.delay = delay

            post.save()
            form.save_m2m()

            images = image_formset.save(commit=False)
            for image in images:
                image.save()

            return redirect('self_user_posts')

        return render(request, self.template_name, {'form': form, 'image_formset': image_formset, 'delay_form': delay_form})


class EditPostView(LoginRequiredMixin, CheckUserConformity,  UpdateView):
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
                    if post.status == Post.STATUS.DEFERRED: post.status = Post.STATUS.PUBLISHED
                    post.save()

            image_formset = ImageFileFormSet(
                request.POST, request.FILES, instance=post)
            images = image_formset.save()

        else:
            delay_form = CreatePostDelayForm()

        return render(request, self.template_name, {'form': form, 'delay_form': delay_form, 'image_formset': ImageFileFormSet(instance=form.instance)})

    def get_form(self, *args, **kwargs):
        return self.get_form_class()(instance=self.object)

    def get_user(self):
        return self.get_object().author


class PostStatisticView(LoginRequiredMixin, CheckUserConformity, DetailView):
    model = Post
    template_name = 'accounts/post_stat.html'
    context_object_name = 'post'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статистика {}'.format(self.object)

        now = timezone.now()
        dates = [now - datetime.timedelta(days=i) for i in range(32)]
        fdates = ['{}.{}'.format(date.month, date.day) for date in dates]
        views_count = self.object.views.count()
        likes_count = self.object.likes.count()

        context['llabels'] = fdates
        context['lvalues'] = [self.object.likes.filter(creation_date__date=date).count() for date in dates]

        context['vlabels'] = fdates
        context['vvalues'] = [self.object.views.filter(creation_date__date=date).count() for date in dates]

        context['clabels'] = fdates
        context['cvalues'] = [self.object.comments.filter(pub_date__date=date).count() for date in dates]

        context['user_kpd'] = round(likes_count / views_count, 4)
        context['views_count'] = views_count
        context['likes_count'] = likes_count
        return context

    def get_user(self):
        return self.get_object().author


class LikedPostList(LoginRequiredMixin, ListView, AnnotateUserLikesMixin):
    model = Post
    paginate_by = 30
    template_name = 'accounts/liked_posts.html'
    context_object_name = 'posts'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return super().get_queryset().filter(likes__user=self.request.user)


from posts.models import PostTag, Post


class DashBoardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = PostTag.objects.all()

        # tags
        context['tlabels'] = [i.name.capitalize() for i in tags]
        context['tvalues'] = [i.related_posts_amount() for i in tags]

        now = timezone.now()
        dates = [now - datetime.timedelta(days=i) for i in range(32)]
        fdates = ['{}.{}'.format(date.month, date.day) for date in dates]
        posts = Post.objects.filter(author=self.request.user)
        subscriptions = Subscription.objects.filter(subscription_object=self.request.user, status=1)

        # views
        context['views_labels'] = fdates
        context['views_values'] = [posts.filter(pub_date__day=date.day, pub_date__month=date.month, pub_date__year=date.year).aggregate(views=Count('views'))['views'] for date in dates]

        # likes
        context['likes_labels'] = fdates
        context['likes_values'] = [posts.filter(pub_date__day=date.day, pub_date__month=date.month, pub_date__year=date.year).aggregate(likes=Count('likes'))['likes'] for date in dates]

        context['sub_labels'] = fdates
        context['sub_values'] = [subscriptions.filter(start_date__day=date.day, start_date__month=date.month, start_date__year=date.year).count() for date in dates]

        return context