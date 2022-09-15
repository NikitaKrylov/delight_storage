from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import *
from mediacore.admin import InlineImageFileAdmin, InlineVideoFileAdmin
from contentcreation.services.generation import ContentGenerator
from mediacore.models import ImageFile

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
    'likes',
)


admin.site.register(Like)


@admin.register(ImagePost)
class ImagePostAdmin(admin.ModelAdmin):
    inlines = [InlineImageFileAdmin]
    list_filter = post_list_filter
    list_display = post_list_display
    readonly_fields = post_readonly_fields
    exclude = post_exclude_fields
    change_form_template = 'posts/image_post_change_form.html'

    def response_generate_image(self, request, post) -> bool:
        if "generate_image" in request.POST:
            cg = ContentGenerator()
            image_file = ImageFile(file=cg.generate(), post=post)
            image_file.save()

            post.files.add(image_file)
            post.save()
            return True
        return False

    def response_change(self, request, post):
        response = self.response_generate_image(request, post)
        if response:
            return HttpResponseRedirect(".")
        return super().response_change(request, post)

    def response_add(self, request, post, post_url_continue=None):
        response = self.response_generate_image(request, post)
        if response:
            return HttpResponseRedirect(reverse("admin:%s_%s_change" %(self.model._meta.app_label, self.model._meta.model_name), args=(post.id,)))
        return super().response_add(request, post, post_url_continue)


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

