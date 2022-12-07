from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.urls import reverse
from django.utils import timezone
from typing import List
from django.utils.translation import gettext_lazy as _


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
    email = models.EmailField(_("email addres"), max_length=255, unique=True)
    avatar = models.ImageField(_("иконка пользователя"), blank=True, null=True)
    birth_date = models.DateField(
        verbose_name=_("дата рождения"), blank=True, null=True)
    start_date = models.DateField(
        verbose_name=_("дата регистрации"), auto_now_add=True)
    ignored_tags = models.ManyToManyField(
        "posts.PostTag", verbose_name=_('игнорируемые теги'), blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def is_adult(self):
        if self.birth_date is None:
            return False
        return (timezone.now().year - self.birth_date.year) > 18

    def get_absolute_url(self):
        return reverse('profile', kwargs={"pk": self.pk})

    def get_unread_notifications(self):
        return self.notifications.filter(unread=True)

    def __str__(self):
        return self.username


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


# class StripSubscription(models.Model):
#    pass