import datetime

from django.core.exceptions import ValidationError
from django.db import models
from accounts.models import User, ClientIP
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Post(models.Model):
    STATUS = (
        (0, _('Опубликованно')),
        (1, _('Отложено')),
        (2, _('На рассмотрении'))
    )

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creation_date = models.DateTimeField(
        _("дата создания"), auto_now_add=True, editable=False)
    pub_date = models.DateTimeField(_('дата публикации'), blank=True, null=True)
    only_for_adult = models.BooleanField(_("18+ контент"), default=False)
    for_autenticated_users = models.BooleanField(
        _("для авторизированных пользователей"), default=False)
    for_premium_users = models.BooleanField(
        _("для премиум пользователей"), default=False)
    disable_comments = models.BooleanField(
        _("запретить коментарии"), default=False)
    status = models.IntegerField(_('статус'), choices=STATUS, default=0, help_text=_('При выборе задержки помечается как "отложено"'))
    description = models.CharField(_('описание'), max_length=300, null=True, blank=True)

    tags = models.ManyToManyField("PostTag", verbose_name=_('теги'), blank=True, null=True)
    views = models.ManyToManyField('UserView', blank=True)
    likes = models.ManyToManyField("Like", verbose_name=_('лайки'), blank=True)
    delay = models.OneToOneField('PostDelay', verbose_name=_('время отложенной публикации'), on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _('пост')
        verbose_name_plural = _('посты')
        ordering = ('-creation_date',)

    def count_media(self) -> int:
        return self.images.count() + self.videos.count()

    def get_absolute_url(self):
        return reverse(viewname=self.__class__._meta.model_name, kwargs={"pk": self.pk})

    def get_absolute_like_url(self):
        return reverse(viewname='post_like', kwargs={"pk": self.pk})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.delay:
            self.status = 1

        return super().save(force_insert, force_update, using, update_fields)

    def clean(self):
        if self.status == 0 and not self.pub_date:
            self.pub_date = timezone.now()

        if self.delay and self.delay.time < timezone.now():
            raise ValidationError("Время публикации не может быть меньше текущего.")

        if self.status == 1 and not self.delay:
            raise ValidationError("Укажите время публикации для отложенного поста")
        return super().clean()

    def __str__(self):
        if self.delay:
            return "Отложенный пост id - {}".format(self.pk)
        return "Пост id - {}".format(self.pk)


class PostDelay(models.Model):
    time = models.DateTimeField(verbose_name=_('Время отложенной публикации'))

    class Meta:
        verbose_name = "Отложенная задача"
        verbose_name_plural = "Отложенные задачи"

    def clean(self):
        if self.time < timezone.now():
            raise ValidationError("Время отложенной задачи не может быть меньше текущей!")
        return super().clean()

    def __str__(self):
        return "Задержка публикации до {}".format(self.time)


# -----------------------COMMENTS----------------------------

class Comment(models.Model):
    author = models.ForeignKey(User, verbose_name=_("автор"), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name=_('комментируемый пост'), on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(verbose_name=_('Дата создания'), auto_now_add=True, editable=False)
    text = models.TextField(_('текст'))
    answered = models.ForeignKey('Comment', on_delete=models.CASCADE, verbose_name=_('Комментируемый комментарий'), related_name='related_comments', blank=True, null=True)

    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"
        ordering = ('-pub_date',)

    def text_length(self):
        return len(self.text)

    text_length.short_description = _('размер')

    def __str__(self):
        if self.answered:
            return "Связанный комментарий от {} -> {}".format(self.author, self.post)
        return "Комментарий от {} -> {}".format(self.author, self.post)


# --------------------TAG--------------------------

class PostTag(models.Model):
    name = models.CharField(_("название тега"), max_length=30, db_index=True, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def related_posts_amount(self):
        return self.post_set.count()

    related_posts_amount.short_description = _('связаных постов')

    def __str__(self):
        return self.name.capitalize()


class Like(models.Model):
    creation_date = models.DateTimeField(_('дата лайка'), auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=_('пользователь'), on_delete=models.SET_NULL, null=True, related_name="likes")

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    @property
    def related_post(self):
        return self.post_set.first()

    def __str__(self):
        return "Лайк от {} -> {}".format(self.user.username, self.related_post)


class UserView(models.Model):
    creation_date = models.DateTimeField(_('дата просмотра'), auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=_('пользователь'), on_delete=models.SET_NULL, null=True, blank=True)
    client_ip = models.ForeignKey(ClientIP, verbose_name=_('IP пользователя'), null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Просмотр пользователя'
        verbose_name_plural = 'Просмотры пользователей'

    @property
    def related_post(self):
        return self.post_set.first()

    def __str__(self):
        return 'Лайкт от {}'.format(self.user or self.client_ip)
