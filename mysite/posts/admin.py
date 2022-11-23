from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import *
from mediacore.admin import InlineImageFileAdmin, InlineVideoFileAdmin
from contentcreation.services.generation import ContentGenerator
from mediacore.models import ImageFile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [InlineImageFileAdmin, InlineVideoFileAdmin]
    list_filter = (
        'tags',
        'only_for_adult',
        'for_autenticated_users',
)
    list_display = (
        'id',
        'creation_date',
        'only_for_adult',
        'for_autenticated_users',
        'disable_comments',
        'status',
    )
    readonly_fields = (
        'creation_date',
    )
    exclude = (
    'views',
    'likes',
    )
    filter_horizontal = ('tags',)
    change_form_template = 'posts/image_post_change_form.html'
    actions = ('make_published', 'put_off',)

    def response_generate_image(self, request, post) -> bool:
        if "generate_image" in request.POST:
            try:
                cg = ContentGenerator()
                image_file = ImageFile(file=cg.generate(), post=post)
                image_file.save()
            except IndexError:
                self.message_user(request, "Ошибка генерации медиа! Список '{}' пуст.".format(cg.last_source_type), level=messages.ERROR)
            else:
                post.images.add(image_file)
                post.save()
            self.message_user(request, 'Медиа файл успешно создан! Ресурс - {}'.format(cg.last_source_name), level=messages.SUCCESS)
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

    def save_model(self, request, post, form, change):
        responce = super().save_model(request, post, form, change)
        if post.images.count() == 0 and post.videos.count() == 0:
            self.message_user(request, '{} должен иметь хотябы один медиа файл!'.format(post), level=messages.WARNING)
        return responce

    @admin.action(description="Опубликовать")
    def make_published(self, request, queryset):
        queryset.update(status=0)

    @admin.action(description="Отложить")
    def put_off(self, request, queryset):
        queryset.update(status=1)


@admin.register(PostDelay)
class PostDelayAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'time',
    )


@admin.register(PostTag)
class TagAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = (
        'related_posts_amount',
    )
    list_display = (
        'name',
        'related_posts_amount',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = (
        'text',
        'author',
    )
    list_display = (
        'id',
        'author',
        'text_length',
        'post',
    )


@admin.register(UserView)
class UserViewAdmin(admin.ModelAdmin):
    search_fields = (
        'user_id',
        'client_ip.ip',
    )
    list_display = (
        'id',
        'user',
        'client_ip',
    )
    list_filter = (
        'user',
        'client_ip',
    )
    readonly_fields = (
        'creation_date',
        'related_post',
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    readonly_fields = (
        'creation_date',
        'related_post',
    )




