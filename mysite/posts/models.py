from django.core.exceptions import ValidationError
from django.db import models
from accounts.models import User, ClientIP
from django.db.models import Count, ExpressionWrapper, FloatField, F
from django.db.models.functions import Cast
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from slugify import slugify


class PostManager(models.Manager):
    def best_by(self, field: str, user: User = None):
        """order posts by views or likes"""
        if user:
            return self.filter(author=user).annotate(value=Count(field)).order_by('value').last()
        return self.annotate(value=Count(field)).order_by('value').last()

    def count_field_elements(self, field: str, user: User = None):
        if user:
            return self.filter(author=user).aggregate(value=Count(field))['value']
        return self.aggregate(value=Count(field))['value']

    def order_by_like_persent(self, **filter):
        return self.annotate(value=Cast(Count(F('likes')), FloatField()) / Cast(Count(F('views')), FloatField()))


class Post(models.Model):

    class STATUS(models.TextChoices):
        PUBLISHED = 'PB', _('опубликовано')
        DEFERRED = 'DF', _('отложено')
        CONSIDERATION = 'CN', _('черновик')

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    creation_date = models.DateTimeField(
        _("дата создания"), auto_now_add=True, editable=False)
    pub_date = models.DateTimeField(
        _('дата публикации'), blank=True, null=True)
    only_for_adult = models.BooleanField(_("18+ контент"), default=False)
    for_autenticated_users = models.BooleanField(
        _("для авторизированных пользователей"), default=False)
    disable_comments = models.BooleanField(
        _("запретить коментарии"), default=False)
    status = models.CharField(_('статус'), choices=STATUS.choices, default=STATUS.CONSIDERATION, help_text=_(
        'При выборе задержки помечается как "отложено"'), max_length=20)
    description = models.CharField(
        _('описание'), max_length=500, null=True, blank=True)

    tags = models.ManyToManyField(
        "PostTag", verbose_name=_('теги'), blank=True, null=True)
    delay = models.OneToOneField('PostDelay', verbose_name=_(
        'время отложенной публикации'), on_delete=models.SET_NULL, null=True, blank=True)

    objects = PostManager()

    class Meta:
        verbose_name = _('пост')
        verbose_name_plural = _('посты')
        ordering = ('-creation_date',)

    def count_media(self) -> int:
        return self.images.count() + self.videos.count()

    def get_absolute_url(self):
        return reverse('post', kwargs={"pk": self.pk})

    def get_absolute_like_url(self):
        return reverse('post_like', kwargs={"pk": self.pk})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.delay:
            self.status = self.STATUS.DEFERRED
        return super().save(force_insert, force_update, using, update_fields)

    def clean(self):
        if self.status == Post.STATUS.PUBLISHED and not self.pub_date:
            self.pub_date = timezone.now()

        if self.delay and self.delay.time < timezone.now():
            raise ValidationError(
                "Время публикации не может быть меньше текущего.")

        if self.status == Post.STATUS.DEFERRED and not self.delay:
            raise ValidationError(
                "Укажите время публикации для отложенного поста")
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
        if self.time and self.time < timezone.now():
            raise ValidationError(
                "Время отложенной задачи не может быть меньше текущей!")
        return super().clean()

    def __str__(self):
        return "Задержка публикации до {}".format(self.time)


# -----------------------COMMENTS----------------------------

class Comment(models.Model):
    author = models.ForeignKey(User, verbose_name=_(
        "автор"), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name=_(
        'комментируемый пост'), on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(verbose_name=_(
        'Дата создания'), auto_now_add=True, editable=False)
    text = models.TextField(_('текст'))
    answered = models.ForeignKey('Comment', on_delete=models.CASCADE, verbose_name=_(
        'Комментируемый комментарий'), related_name='related_comments', blank=True, null=True)

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


class PostTagManager(models.Manager):

    def best_by(self, field: str, user: User = None):
        if not user or not user.is_authenticatedr:
            return self.annotate(value=Count('post__{}'.format(field))).order_by('-value')
        return self.filter(author=user).annotate(value=Count('post__{}'.format(field))).order_by('-value')


class PostTag(models.Model):
    name = models.CharField(
        _("название тега"), max_length=30, db_index=True, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def related_posts_amount(self):
        return self.post_set.count()

    related_posts_amount.short_description = _('связаных постов')

    objects = PostTagManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name.capitalize()


class Like(models.Model):
    post = models.ForeignKey(Post, models.CASCADE, 'likes')
    creation_date = models.DateTimeField(_('дата лайка'), auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=_(
        'пользователь'), on_delete=models.SET_NULL, null=True, related_name="likes")

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return "Лайк от {} -> {}".format(self.user.username if self.user else 'Удален', self.post)


class UserView(models.Model):
    post = models.ForeignKey(Post, models.CASCADE, 'views')
    creation_date = models.DateTimeField(
        _('дата просмотра'), auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=_(
        'пользователь'), on_delete=models.SET_NULL, null=True, blank=True)
    client_ip = models.ForeignKey(ClientIP, verbose_name=_(
        'IP пользователя'), null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Просмотр пользователя'
        verbose_name_plural = 'Просмотры пользователей'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not (self.user or self.client_ip):
            raise ValueError("Нужно указать субъекта")
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return 'Лайкт от {} -> {}'.format(self.user or self.client_ip, self.post)
