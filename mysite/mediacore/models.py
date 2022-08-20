from django.db import models
from posts.models import VideoPost, ImagePost
from accounts.models import ContentAuthor
import os
from django.utils.translation import gettext_lazy as _
from .services import compress
from django.dispatch import receiver

file_post_help_text = 'файл обязательно должен быть прикреплен к посту'


class ImageFile(models.Model):
    title = models.CharField(_('заголовок'), max_length=60, blank=True)
    file = models.ImageField(_('файл'), upload_to="images")
    use_compression = models.BooleanField(
        _('использовать компрессию'), default=False)
    post = models.ForeignKey(
        ImagePost, on_delete=models.CASCADE, help_text=_(file_post_help_text), related_name='files')
    compressed = models.BooleanField(default=False)
    content_author = models.ForeignKey(verbose_name=_(
        'автор изображения'), to=ContentAuthor, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def save(self, *args, **kwargs):
        if self.use_compression and not self.compressed:
            new_image = compress(self.file)
            self.file = new_image
            self.compressed = True

        return super().save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)

    def file_size(self):
        return self.file.size

    def clean(self):
        return super().clean()

    def __str__(self):
        return self.filename()


class VideoFile(models.Model):
    title = models.CharField(_('заголовок'), max_length=60, blank=True)
    file = models.FileField(_('файл'), upload_to="videos")
    content_author = models.ForeignKey(
        ContentAuthor, verbose_name=_('автор изображения'), on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey(
        VideoPost, on_delete=models.CASCADE, help_text=_(file_post_help_text), related_name='files')

    class Meta:
        verbose_name = "Видео файл"
        verbose_name_plural = "Видео файлы"

    def filename(self):
        return os.path.basename(self.file.name)

    def file_size(self):
        return self.file.size

    def __str__(self):
        return self.filename()


@receiver(models.signals.post_delete, sender=ImageFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=ImageFile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False


@receiver(models.signals.post_delete, sender=VideoFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=VideoFile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
