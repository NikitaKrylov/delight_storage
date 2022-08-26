from django.contrib import admin
from .models import *
from mediacore.admin import InlineImageFileAdmin, InlineVideoFileAdmin

post_list_filter = (
    'tags',
    'only_for_adult',
    'for_autenticated_users',
    'for_premium_users',
)
post_list_display = (
    'id',
    'publication_date',
    'only_for_adult',
    'for_autenticated_users',
    'disable_comments',
    'count_tags',
    'count_comments',
    'count_likes',
    'count_views',
)
post_readonly_fields = (
    'count_comments',
    'count_likes',
    'count_views',
    'count_views',
)
post_exclude_fields = (
    'views',
)


admin.site.register(Like)

@admin.register(ImagePost)
class ImagePostAdmin(admin.ModelAdmin):
    inlines = [InlineImageFileAdmin]
    list_filter = post_list_filter
    list_display = post_list_display
    readonly_fields = post_readonly_fields
    exclude = post_exclude_fields


@admin.register(VideoPost)
class VideoPostAdmin(admin.ModelAdmin):
    inlines = [InlineVideoFileAdmin]
    list_filter = post_list_filter
    list_display = post_list_display
    readonly_fields = post_readonly_fields
    exclude = post_exclude_fields


@admin.register(TextPost)
class TextPostAdmin(admin.ModelAdmin):
    search_fields = (
        'title',
        'body'
    )
    list_filter = post_list_filter
    list_display = post_list_display
    readonly_fields = post_readonly_fields
    exclude = post_exclude_fields


@admin.register(PostTag)
class TagAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
    )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = (
        'text',
        'author',
    )
    list_display = (
        'author',
        'content_type',
        'object_id',
        'text_length',
    )

