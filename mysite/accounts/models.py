import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models import QuerySet
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from typing import List, Union
from django.utils.translation import gettext_lazy as _
from notifications.base.models import AbstractNotification
from mysite.errors import IncorrectDeletionError


class UserManager(BaseUserManager):
    def create_user(self, email: str, username: str, password: str = None, **other_field):
        if not email:
            raise ValueError(_("Нужно указать email адресс"))

        email = self.normalize_email(email)
        user: User = self.model(email=email, username=username, **other_field)
        user.is_active = True
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, username: str, password: str, **other_field):
        other_field.setdefault("is_staff", True)
        other_field.setdefault("is_superuser", True)
        other_field.setdefault("is_active", True)

        if other_field.get("is_staff") is not True:
            raise ValueError("Superuser должен быть создан с параметром is_staff=True.")

        if other_field.get("is_superuser") is not True:
            raise ValueError(
                "Superuser должен быть создан с параметром is_superuser=True.")

        return self.create_user(email, username, password, **other_field)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('имя пользователя'), max_length=50, unique=True)
    email = models.EmailField(_("почта"), max_length=255, unique=True)
    avatar = models.ImageField(_("иконка пользователя"), upload_to='users_avatars/', blank=True, null=True)
    birth_date = models.DateField(
        verbose_name=_("дата рождения"), blank=True, null=True)
    start_date = models.DateField(
        verbose_name=_("дата регистрации"), auto_now_add=True, editable=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    role = models.ForeignKey('Role', verbose_name=_('роль'), on_delete=models.SET_NULL, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def is_adult(self):
        if self.birth_date is None:
            return False
        return (timezone.now().year - self.birth_date.year) >= 18

    def get_absolute_url(self):
        return reverse('profile', kwargs={"pk": self.pk})

    def get_unread_notifications(self):
        return self.notifications.filter(unread=True)

    def __str__(self):
        return self.username


class UserSettings(models.Model):
    user = models.OneToOneField(User, related_name="settings", on_delete=models.CASCADE)
    ignored_tags = models.ManyToManyField(
        "posts.PostTag", verbose_name=_('игнорируемые теги'), blank=True)
    user_card_image = models.ImageField(upload_to='users_card_images/', blank=True, null=True)
    notify_on_post_commented = models.BooleanField(_('Уведомлять о новом комментарии к посту'), default=True)
    notify_on_comment_reply = models.BooleanField(_('Уведомлять об ответе на комментарий'), default=True)

    def delete(self, using=None, keep_parents=False):
        raise IncorrectDeletionError("You cannot delete \"UserSettings\" model manually, deletion is possible by cascading deletion through the user model")

    def __str__(self):
        return 'Настройки пользователя {}'.format(self.user.username)


class Role(models.Model):
    name = models.CharField(_("название"), max_length=50)
    image = models.ImageField(_("иконка"), null=True, blank=True)
    color = models.CharField(_("цвет"), max_length=7, help_text=_("цвет указывается в hex формате"), default="#fff")
    description = models.CharField(_("описание"), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('роль')
        verbose_name_plural = _('роли')

    def __str__(self):
        return self.name


def check_role(user: User, role: Union[Role, str]):
    if isinstance(role, Role):
        return user.role == role
    elif isinstance(role, str):
        return user.role and user.role.name == role

    return False


def check_roles(user, roles: List[Union[Role, str]], complete_match=False):
    rez = [check_role(user, role) for role in roles]
    return all(rez) if complete_match else any(rez)


class FolderPost(models.Model):
    post = models.ForeignKey('posts.Post', models.CASCADE, verbose_name=_('пост'))
    folder = models.ForeignKey('Folder', models.CASCADE, related_name='posts', verbose_name=_('папка'))
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('дата добавления'))

    class Meta:
        verbose_name = _('пост папки')
        verbose_name_plural = _('посты папки')
        ordering = ('-created',)

    def __str__(self):
        return "{} папки '{}'".format(str(self.post), self.folder.name)


class Folder(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='folders', verbose_name=_('пользователь'))
    name = models.CharField(max_length=30, verbose_name=_('Название'))
    icon = models.ImageField(_('иконка'), blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('описание'))
    is_private = models.BooleanField(_('приватная папка'), default=True, help_text=_('другие пользователи смогут видеть содержимое папки'))
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('дата создания'))

    class Meta:
        verbose_name = _('папка пользователя')
        verbose_name_plural = _('папки пользователей')
        ordering = ('-created',)

    def add(self, obj: Union['posts.Post', FolderPost, QuerySet]):
        if isinstance(obj, FolderPost):
            obj.folder = self
            obj.save()

        elif isinstance(obj, QuerySet):
            FolderPost.objects.bulk_create([
                FolderPost(post=post, folder=self) for post in obj.all()
            ])

        else:
            FolderPost.objects.create(post=obj, folder=self)

    def remove(self, obj):
        if isinstance(obj, FolderPost):
            obj.delete()
        else:
            self.posts.filter(post__id=obj.id).delete()

    def __contains__(self, item):
        if isinstance(item, FolderPost):
            return self.posts.filter(id=item.id).exists()

        return self.posts.filter(post__id=item.id).exists()

    def get_absolute_url(self):
        return reverse('user_folder', kwargs={'pk': self.pk})

    def __str__(self):
        return "Папка '{}' пользователя {}".format(self.name, str(self.user))


@receiver(models.signals.post_delete, sender=Folder)
def auto_delete_file_on_delete(sender, instance: Folder, **kwargs):
    if instance.icon:
        if os.path.isfile(instance.icon.path):
            os.remove(instance.icon.path)


class ClientIP(models.Model):
    ip = models.CharField(_('адрес'), max_length=100)

    class Meta:
        verbose_name = 'IP Клиента'
        verbose_name_plural = 'IP Клиентов'

    def __str__(self):
        return self.ip


class Subscription(models.Model):
    STATUS = (
        (0, 'Неактивная'),
        (1, 'Активная'),
    )
    start_date = models.DateTimeField(_("Дата начала подписки"), auto_now_add=True, editable=False)
    subscription_object = models.ForeignKey(User, verbose_name=_("Объект подписи"), on_delete=models.CASCADE, related_name='user_subscriptions')
    subscriber = models.ForeignKey(User, verbose_name=_("Подписчик"), on_delete=models.CASCADE, related_name='subscriptions')
    status = models.IntegerField(_("статус"), choices=STATUS, default=1)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    @property
    def sub_time_delta(self):
        return timezone.now() - self.start_date if timezone.now() and self.start_date else 'Нет данных'

    def __str__(self):
        return "Подписка на {} от {}".format(self.subscription_object, self.subscriber)


class Notification(AbstractNotification):
    class Types(models.TextChoices):
        SUBSCRIPTION = 'SB', _('Подписка')
        NEW_POST = 'NP', _('Новый пост')
        ACCOUNT = 'AC', _('Аккаунт')
        COMMENT = 'CM', _('Комментарий')
        COMPLAINT = 'CP', _("Жалоба")

    type = models.CharField(_("тип уведомления"), choices=Types.choices, max_length=10)

    class Meta(AbstractNotification.Meta):
        abstract = False
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def clean(self):
        if self.type is None:
            raise ValueError("Тип уведомления должен быть указан")
        return super().clean()

    def __str__(self):
        return self.verb


class PostComplaint(models.Model):
    class Meta:
        verbose_name = "Жалоба на пост"
        verbose_name_plural = "Жалобы на посты"

    class Status(models.TextChoices):
        CONSIDERATION = 'CN', _('На рассмотрении')
        ACCEPTED = 'AC', _('Принята')
        REJECTED = 'RJ', _('Отклонена')

    class Types(models.TextChoices):
        BAD_TAG = 'BT', _('Несоответствие тегам')
        BAD_MEDIA = 'BM', _('Неподходящие/плохие медиа')
        PLAGIAT = 'PL', _('Плагиат')
        ANOTHER = 'AN', _("Другое")

    status = models.CharField(_('статус'), choices=Status.choices, max_length=20, default=Status.CONSIDERATION)
    type = models.CharField(_('тип жалобы'), choices=Types.choices, default=Types.BAD_TAG, max_length=40)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='complaints', verbose_name=_('пост'))
    sender = models.ForeignKey(User, verbose_name=_('отправитель'), on_delete=models.CASCADE, related_name='complaints')
    creation_date = models.DateTimeField(_('дата создания'), editable=False, auto_now_add=True)
    description = models.TextField(_('описание'), max_length=200, null=True, blank=True)

    def __str__(self):
        return 'Жалоба на {} от {}'.format(self.post, self.sender)


