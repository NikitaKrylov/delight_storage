from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
import os
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from mysite.settings import POST_MEDIA_PATH, ALLOWED_EXTENSIONS

file_post_help_text = 'файл обязательно должен быть прикреплен к посту'


class ImageFile(models.Model):
    file = models.ImageField(_('файл'), upload_to=POST_MEDIA_PATH, validators=[
        FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)
    ])
    post = models.ForeignKey(
        'posts.Post', on_delete=models.CASCADE, help_text=_(file_post_help_text), related_name='images', null=True, blank=True)
    compressed = models.BooleanField(_('Использование компресии'), default=False)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def filename(self):
        return os.path.basename(self.file.name)

    def file_size(self):
        return self.file.size

    def get_absolute_url(self):
        return reverse(viewname='post', kwargs={"pk": self.post.pk})

    def __str__(self):
        return self.filename()


class VideoFile(models.Model):
    file = models.FileField(_('файл'), upload_to=POST_MEDIA_PATH)
    post = models.ForeignKey(
        'posts.Post', on_delete=models.CASCADE, help_text=_(file_post_help_text), related_name='videos')

    class Meta:
        verbose_name = "Видео файл"
        verbose_name_plural = "Видео файлы"

    def filename(self):
        return os.path.basename(self.file.name)

    def file_size(self):
        return self.file.size

    def __str__(self):
        return self.filename()