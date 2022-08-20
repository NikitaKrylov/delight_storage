from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from typing import List
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email: str, username: str, password: str, **other_field):
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user: User = self.model(email=email, username=username, **other_field)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, username: str, password: str, **other_field):
        other_field.setdefault("is_staff", True)
        other_field.setdefault("is_superuser", True)
        other_field.setdefault("is_active", True)

        if other_field.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")

        if other_field.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, username, password, **other_field)


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(_("email addres"), max_length=255, unique=True)
    avatar = models.ImageField(_("иконка пользователя"), blank=True, null=True)
    birth_date = models.DateField(
        verbose_name="дата рождения", blank=True, null=True)
    start_date = models.DateField(
        verbose_name="дата регистрации", auto_now_add=True)
    ignored_tags = models.ManyToManyField(
        "posts.PostTag", verbose_name=_('игнорируемые теги'), null=True)

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

    def __str__(self):
        return self.username


class ContentAuthor(models.Model):

    name = models.CharField(_("автор контента"), max_length=60)
    url = models.URLField(_("ссылка на ресурс автора"), blank=True, null=True)

    class Meta:
        verbose_name = "Автор контента"
        verbose_name_plural = "Авторы контента"
