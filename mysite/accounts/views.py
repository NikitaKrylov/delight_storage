from django.contrib import messages
from django.db.models import Count, Sum
from django.views.decorators.http import require_http_methods
from posts.models import PostTag, Post
import datetime
from mysite.services import ajax_require
import json
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from .mixins import CheckUserConformity
from .models import Notification, Folder
from .forms import RegisterUserForm, AuthenticationUserForm, EditUserProfileForm, UserPasswordResetForm, \
    UserSetPasswordForm, UserSettingsForm, UserFolderForm
from .models import User, Subscription
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView
from posts.models import Post, Comment, Like, UserView
from mediacore.forms import ImageFileFormSet, VideoFileFormSet
from posts.forms import PostForm
from django.contrib.auth import login, authenticate
from accounts.services.base import ChartStatistic
from posts.mixins import PostFilterFormMixin
from posts.forms import CreatePostTagForm
from posts.mixins import PostListMixin


@login_required
@require_http_methods(['GET'])
def switch_subscription(request, *args, **kwargs):
    ctx = {"has_sub": None}
    user: User = request.user

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

    return JsonResponse(ctx)

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
        user = authenticate(
            username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
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


# --------------- User Folders-----------------


class UserFoldersListView(LoginRequiredMixin, PostFilterFormMixin, ListView):
    template_name = 'accounts/folders/user_folders.html'
    context_object_name = 'folders'
    model = Folder

    def get_queryset(self):
        return self.request.user.folders.all()


class UserFolderView(LoginRequiredMixin, PostFilterFormMixin, DetailView):
    template_name = 'accounts/folders/user_folder.html'
    context_object_name = 'folder'
    model = Folder

    def get_context_data(self, **kwargs):
        context = super(UserFolderView, self).get_context_data(**kwargs)
        context['folder_posts'] = self.get_object().posts.all()
        context['folder_form'] = UserFolderForm(instance=self.get_object())
        return context


class CreateUserFolderView(LoginRequiredMixin, PostFilterFormMixin, CreateView):
    model = Folder
    form_class = UserFolderForm
    template_name = 'accounts/folders/create_folder.html'
    success_url = reverse_lazy('user_folders')

    def form_valid(self, form):
        self.object: Folder = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.success(self.request, "Папка '{}' создана.".format(self.object.name))
        return super().form_valid(form)

@ajax_require
def create_folder_ajax(request, *args, **kwargs):
    folder  = UserFolderForm(request.POST)
    if form.is_valid():
        folder = form.create()
        return JsonResponse({"id": folder.id, "name" : folder.name})
    response = JsonResponse({"errors": list(form.errors.values())})
    response.status_code = 403
    return response


@login_required
def delete_folder(request, *args, **kwargs):
    folder = request.user.folders.filter(pk=kwargs['pk'])
    messages.success(request, "Папка '{}' удалена.".format(folder.first().name))
    folder.delete()

    return redirect('user_folders')


@require_http_methods(["POST"])
def edit_folder(request, *args, **kwargs):
    form = UserFolderForm(request.POST, instance=request.user.folders.get(pk=kwargs['pk']))
    if form.is_valid():
        folder = form.save()
        return redirect('user_folder', pk=folder.pk)


@login_required
def add_to_folder(request, *args, **kwargs):
    folder = request.user.folders.get(id=kwargs['folder'])
    post = Post.objects.get(id=kwargs['post'])

    if post not in folder:
        folder.add(post)

    return JsonResponse({'post': post.id, 'folder': folder.name})


@login_required
def remove_from_folder(request, *args, **kwargs):
    folder = request.user.folders.get(id=kwargs['folder'])
    post = Post.objects.get(id=kwargs['post'])

    if post in folder:
        folder.remove(post)

    return redirect('user_folder', pk=folder.id)

# --------------User Info---------------


class UserInfoView(DetailView):
    model = User
    template_name ='accounts/user_info/user_info.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(UserInfoView, self).get_context_data(**kwargs)
        posts = Post.objects.filter(author=self.object).exclude(status=Post.STATUS.DEFERRED)
        context['posts'] = posts
        context['likes_count'], context['views_count'], context['comments_count'] = posts.aggregate(
            likes_count=Count('likes'),
            views_count=Count('views'),
            comments_count=Count('comments')
        ).values()

        return context


class UserPostList(PostListMixin, PostFilterFormMixin, ListView):
    model = Post
    template_name = 'accounts/user_info/user_posts.html'
    context_object_name = 'posts'

    def get_context_data(self, *args, **kwargs):
        context = super(UserPostList, self).get_context_data(*args, **kwargs)
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        context['user'] = user
        context['sub_count'] = user.user_subscriptions.count()
        context['likes_count'] = self.object_list.aggregate(lc=Sum('likes_amount'))['lc']
        return context

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return super().get_queryset().filter(author=user)


# --------------User Page---------------


class UserProfileView(LoginRequiredMixin, PostFilterFormMixin, FormView):
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
        form = EditUserProfileForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('profile')


@login_required(login_url=reverse_lazy('login'))
def edit_user_form(request, *args, **kwargs):
    ctx = {}
    form = EditUserProfileForm(
        request.POST, request.FILES, instance=request.user)

    ctx['has_changed'] = form.has_changed()
    if form.is_valid() and form.has_changed():
        form.save()
    return HttpResponse(json.dumps(ctx), content_type='application/json')


class UserNotificationListView(LoginRequiredMixin, PostFilterFormMixin, ListView):
    model = Notification
    context_object_name = 'notifications'
    login_url = reverse_lazy('login')
    template_name = 'accounts/notifications.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Уведомления'
        user = self.request.user
        context['unread'] = user.notifications.filter(
            unread=True, deleted=False)
        context['readed'] = user.notifications.filter(
            unread=False, deleted=False)
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
    notifications = request.user.notifications.filter(deleted=False)

    if notifications.count() > 0:
        messages.success(request, 'Удалено уведомлений - {}'.format(notifications.count()))
    else:
        messages.info(request, "Список уведомлений пуст")

    notifications.update(deleted=True, unread=False)
    return redirect('user_notifications')


@login_required(login_url=reverse_lazy('login'))
def read_all_notification(request, *args, **kwargs):
    notifications = request.user.notifications.filter(deleted=False, unread=True)

    if notifications.count() > 0:
        messages.success(request, 'Уведомлениый прочитано - {}'.format(notifications.count()))
    else:
        messages.info(request, "Список уведомлений пуст")

    notifications.update(unread=False)
    return redirect('user_notifications')


class SelfUserPostListView(LoginRequiredMixin, PostListMixin, PostFilterFormMixin, ListView):
    model = Post
    login_url = reverse_lazy('login')
    context_object_name = 'posts'
    template_name = 'accounts/self_user_posts.html'
    mark_liked = False
    check_availability = False
    post_status = None

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_context_data(self, *args, object_list=None, **kwargs):
        self.queryset = self.get_queryset()
        user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Мои посты'
        context['likes_amount'] = Post.objects.count_field_elements(
            'likes', user)
        context['views_amount'] = Post.objects.count_field_elements(
            'views', user)
        context['comments_amount'] = Post.objects.count_field_elements(
            'comments', user)

        end = timezone.now().date()
        start = end - datetime.timedelta(days=7)
        # views
        context['dates'], context['views_values'] = ChartStatistic(Like.objects.filter(post__author=user), 'creation_date', start, end).create()
        context['likes_values'] = ChartStatistic(UserView.objects.filter(post__author=user), 'creation_date', start, end).create().values
        context['comments_values'] = ChartStatistic(Comment.objects.filter(post__author=user), 'pub_date', start, end).create().values

        return context


class UserSettingsFormView(LoginRequiredMixin, PostFilterFormMixin, FormView):
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


class UserSubscriptionListView(LoginRequiredMixin, PostFilterFormMixin, ListView):
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
        context['video_formset'] = VideoFileFormSet()
        context['tag_form'] = CreatePostTagForm()
        return context

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        image_formset = ImageFileFormSet(
            request.POST, request.FILES, instance=form.instance)
        video_formset = VideoFileFormSet(
            request.POST, request.FILES, instance=form.instance)

        if form.is_valid() and (image_formset.is_valid() or video_formset.is_valid()):
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            form.save_m2m()

            if image_formset.is_valid():
                for image in image_formset.save(commit=False):
                    image.save()

            if video_formset.is_valid():
                for video in video_formset.save(commit=False):
                    video.save()

            messages.success(request, "{} создан.".format(str(post)))
            return redirect('self_user_posts')
        return render(request, self.template_name, {'form': form, 'image_formset': image_formset})


class EditPostView(LoginRequiredMixin, CheckUserConformity,  UpdateView):
    model = Post
    login_url = reverse_lazy('login')
    template_name = 'accounts/post_change.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post'] = post

        context['title'] = str(post)

        context['image_formset'] = ImageFileFormSet(instance=post)
        context['video_formset'] = VideoFileFormSet(instance=post)
        context['tag_form'] = CreatePostTagForm()

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST, instance=self.get_object())
        image_formset = ImageFileFormSet(
            request.POST, request.FILES, instance=form.instance)
        video_formset = VideoFileFormSet(
            request.POST, request.FILES, instance=form.instance)

        if form.is_valid():
            post = form.save()

            if image_formset.is_valid():
                for image in image_formset.save(commit=False):
                    image.save()

            if video_formset.is_valid():
                for video in video_formset.save(commit=False):
                    video.save()

        else:
            return render(request, self.template_name, {'form': form, 'image_formset': ImageFileFormSet(instance=form.instance)})

        messages.success(request, "{} изменен.".format(str(post)))
        return redirect('self_user_posts')

    def get_form(self, *args, **kwargs):
        return self.get_form_class()(instance=self.object)


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
        fdates = ['{}.{}'.format(date.day, date.month) for date in dates]
        views_count = self.object.views.count()
        likes_count = self.object.likes.count()

        context['llabels'] = fdates
        context['lvalues'] = [self.object.likes.filter(
            creation_date__date=date).count() for date in dates]

        context['vlabels'] = fdates
        context['vvalues'] = [self.object.views.filter(
            creation_date__date=date).count() for date in dates]

        context['clabels'] = fdates
        context['cvalues'] = [self.object.comments.filter(
            pub_date__date=date).count() for date in dates]

        context['user_kpd'] = round(likes_count / views_count, 4)
        context['views_count'] = views_count
        context['likes_count'] = likes_count
        return context

    def get_user(self):
        return self.get_object().author


class LikedPostList( PostListMixin, LoginRequiredMixin, PostFilterFormMixin, ListView):
    model = Post
    paginate_by = 30
    template_name = 'accounts/liked_posts.html'
    context_object_name = 'posts'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return super().get_queryset().filter(likes__user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Лайки'
        return context


class DashBoardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        tags = PostTag.objects.all()

        context['tlabels'] = [i.name.capitalize() for i in tags]
        context['tvalues'] = [i.related_posts_amount() for i in tags]

        end = timezone.now().date()
        start = end - datetime.timedelta(days=31)

        context['views_labels'], context['views_values'] = ChartStatistic(UserView.objects.filter(post__author=user), 'creation_date', start, end).create()
        context['likes_labels'], context['likes_values'] = ChartStatistic(Like.objects.filter(post__author=user), 'creation_date', start, end).create()
        context['sub_labels'], context['sub_values'] = ChartStatistic(Subscription.objects.filter(subscription_object=user), 'start_date', start, end).create()

        return context
