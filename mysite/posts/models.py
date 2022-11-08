from django.db import models
from accounts.models import User, ClientIP
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet
from django.urls import reverse
from django.core.exceptions import ValidationError


class PostManager(models.Manager):
    def contain_tags(self, *tags) -> QuerySet:
        return self.get_queryset().filter(tags__name__in=tags).order_by("-publication_date")

    def get_by_author(self, author: User):
        return self.get_queryset().filter(post_author=author).order_by("-publication_date")


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    publication_date = models.DateField(
        _("дата публикации"), auto_now_add=True)
    only_for_adult = models.BooleanField(_("18+ контент"), default=False)
    for_autenticated_users = models.BooleanField(
        _("для авторизированных пользователей"), default=False)
    for_premium_users = models.BooleanField(
        _("для премиум пользователей"), default=False)
    disable_comments = models.BooleanField(
        _("запретить коментарии"), default=False)
    description = models.CharField(_('описание'), max_length=300, null=True, blank=True)

    tags = models.ManyToManyField("PostTag", verbose_name=_('теги'), blank=True, null=True)
    comments = GenericRelation("Comment")
    views = models.ManyToManyField(ClientIP, blank=True)
    likes = models.ManyToManyField("Like", verbose_name=_('лайки'), blank=True)

    objects = PostManager()

    class Meta:
        verbose_name = _('пост')
        verbose_name_plural = _('посты')

    def count_likes(self) -> int:
        return self.likes.count()

    def count_views(self) -> int:
        return self.views.count()

    def count_comments(self) -> int:
        return self.comments.count()

    def count_tags(self) -> int:
        return self.tags.count()

    def count_media(self) -> int:
        return self.images.count() + self.videos.count()

    def get_tags(self):
        return self.tags.all()

    def get_images(self):
        return self.images

    def get_videos(self):
        return self.videos

    def converted_date(self) -> str:
        pass

    def get_absolute_url(self):
        return reverse(viewname=self.__class__._meta.model_name, kwargs={"pk": self.pk})

    def get_absolute_like_url(self):
        return reverse(viewname='post_like', kwargs={"pk": self.pk})

    def __str__(self):
        return "Пост id - {}".format(self.pk)


# -----------------------COMMENTS----------------------------

class Comment(models.Model):
    author = models.ForeignKey(User, verbose_name=_("автор"), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name=_('комментируемый пост'), on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(verbose_name=_('Дата комментария'), auto_now_add=True)
    text = models.TextField(_('текст'))
    answered = models.ForeignKey('Comment', on_delete=models.CASCADE, verbose_name=_('Комментируемый комментарий'), related_name='related_comments', blank=True, null=True)

    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"

    def text_length(self):
        return len(self.text)


# --------------------TAG--------------------------

class PostTag(models.Model):
    name = models.CharField(_("название тега"), max_length=30, db_index=True, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name.capitalize()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="likes")

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    def __str__(self):
        return "Лайк от {}".format(self.user.username)
