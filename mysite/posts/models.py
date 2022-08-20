from django.db import models
from accounts.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg, QuerySet
from django.core.validators import MaxValueValidator
from typing import List
from django.urls import reverse
from django.core.exceptions import ValidationError


class PostManager(models.Manager):
    def contain_tags(self, *tags) -> QuerySet:
        return self.get_queryset().filter(tags__name__in=tags).order_by("-publication_date")

    def get_by_author(self, author: User):
        return self.get_queryset().filter(post_author=author).order_by("-publication_date")


class AbstractBasePost(models.Model):
    publication_date = models.DateField(
        _("дата публикации"), auto_now_add=True)
    post_author = models.ForeignKey(User, verbose_name=_('автор поста'), on_delete=models.PROTECT)
    only_for_adult = models.BooleanField(_("18+ контент"), default=False)
    for_autenticated_users = models.BooleanField(
        _("для авторизированных пользователей"), default=False)
    for_premium_users = models.BooleanField(
        _("для премиум пользователей"), default=False)
    disable_comments = models.BooleanField(
        _("запретить коментарии"), default=False)

    tags = models.ManyToManyField("PostTag", verbose_name=_('теги'))
    comments = GenericRelation("Comment")
    marks = GenericRelation("Mark")

    objects = PostManager()

    class Meta:
        abstract = True

    def count_comments(self) -> int:
        return self.comments.count()

    def count_tags(self) -> int:
        return self.tags.count()

    def count_marks(self) -> int:
        return self.marks.count()

    def average_mark(self) -> float:
        value_avg = self.marks.aggregate(Avg('value'))['value__avg']
        return 0 if value_avg is None else value_avg

    def get_tags(self) -> List:
        return self.marks.all()

    def get_absolute_url(self):
        return reverse(viewname=self.__class__._meta.model_name, kwargs={"pk": self.pk})


class ImagePost(AbstractBasePost):
    class Meta:
        verbose_name = "Фото пост"
        verbose_name_plural = "Фото посты"

    def __str__(self):
        return 'Фото пост id - {}'.format(self.pk)


class VideoPost(AbstractBasePost):
    class Meta:
        verbose_name = "Видео пост"
        verbose_name_plural = "Видео посты"

    def __str__(self):
        return 'Видео пост id - {}'.format(self.pk)


class TextPost(AbstractBasePost):
    title = models.CharField(_("заголовок"), max_length=150)
    body = models.TextField(_("текст"), blank=True, null=True)

    class Meta:
        verbose_name = "Текстовые пост"
        verbose_name_plural = "Текстовые посты"

    def __str__(self):
        return 'Текстовый пост id - {}'.format(self.pk)


# -----------------------COMMENTS----------------------------

class Comment(models.Model):
    author = models.ForeignKey(User, verbose_name=_("автор"), on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, verbose_name=_('тип коментируемого объекта'),
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(_('id объекта'))
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(_('текст'))

    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"

    def text_length(self):
        return len(self.text)

    def clean(self):
        if self.content_object is None:
            raise ValidationError(f"{self.content_type.name} c id {self.object_id} не найден")

        return super().clean()


class Mark(models.Model):
    value = models.PositiveBigIntegerField(_("оценка"), validators=(MaxValueValidator(5),))
    author = models.ForeignKey(User, verbose_name=_("автор оценки"), on_delete=models.SET_NULL, null=True)

    content_type = models.ForeignKey(ContentType, verbose_name='тип оцениваемого объекта', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name=_('id объекта'))
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

    def __str__(self):
        return "{} оценил на {}".format(self.author, self.value)


# --------------------TAG--------------------------

class PostTag(models.Model):
    name = models.CharField(_("название тега"), max_length=30, db_index=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name
