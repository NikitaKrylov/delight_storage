from tempfile import NamedTemporaryFile
from django.core.files import File
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
import os
from django.utils.translation import gettext_lazy as _
from mysite.settings import POST_MEDIA_PATH, ALLOWED_EXTENSIONS, MEDIA_ROOT
import cv2
from django.core.files.storage import default_storage
from pathlib import Path

file_post_help_text = 'файл обязательно должен быть прикреплен к посту'


class ImageFile(models.Model):
    file = models.ImageField(_('файл'), upload_to=POST_MEDIA_PATH, validators=[
        FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)
    ])
    post = models.ForeignKey(
        'posts.Post', on_delete=models.CASCADE, help_text=_(file_post_help_text), related_name='images', null=True,
        blank=True)
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
    thumbnail = models.ImageField(upload_to=POST_MEDIA_PATH, null=True, blank=True)

    class Meta:
        verbose_name = "Видео файл"
        verbose_name_plural = "Видео файлы"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.thumbnail:
            print('generate thumbnails')
            self._create_thumbnail()

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def file_size(self):
        return self.file.size

    def _create_thumbnail(self):
        file_name = Path(self.file.name).stem + '_thumbnail.jpg'
        file_path = os.path.join(MEDIA_ROOT, file_name)

        success, image = cv2.VideoCapture(self.file.path).read()
        cv2.imwrite(file_path, image)

        with NamedTemporaryFile() as temp_file:
            with open(file_path, 'rb') as file:
                temp_file.write(file.read())

            self.thumbnail.save(file_name, File(temp_file), save=True)

        default_storage.delete(file_name)

    def __str__(self):
        return self.filename
