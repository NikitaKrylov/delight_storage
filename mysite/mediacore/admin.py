from django.contrib import admin
from django.core.exceptions import ValidationError

from mysite.settings import MAX_FILES_IN_IMAGE_POST, MAX_FILES_IN_VIDEO_POST, MAX_IMAGE_BAIT_SIZE
from .models import ImageFile, VideoFile
from django.utils.safestring import mark_safe


class InlineImageFileAdmin(admin.StackedInline):
    model = ImageFile
    extra = 0
    min_num = 0
    max_num = MAX_FILES_IN_IMAGE_POST
    readonly_fields = (
        'compressed',
        'file_image',
    )
    image_scale = .3

    def file_image(self, obj: ImageFile):
        return mark_safe('<img src="{url}" width="{width}" height="{height}" />"'.format(
            url=obj.file.url,
            width=obj.file.width * self.image_scale,
            height=obj.file.height * self.image_scale,
        ))


@admin.register(ImageFile)
class ImageFileAdmin(admin.ModelAdmin):
    search_fields = (
        'file',
    )
    readonly_fields = (
        'compressed',
        'file_image',
    )
    list_display = (
        'filename',
        'file_size',
        'compressed',
    )

    def file_image(self, obj: ImageFile):
        return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
            url=obj.file.url,
            width=obj.file.width,
            height=obj.file.height,
        ))


class InlineVideoFileAdmin(admin.StackedInline):
    model = VideoFile
    extra = 0
    min_num = 0
    max_num = MAX_FILES_IN_VIDEO_POST


@admin.register(VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
    search_fields = (
        'file',
    )
    list_display = (
        'filename',
        'file_size',
    )
