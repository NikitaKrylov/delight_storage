from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import *
from mediacore.admin import InlineImageFileAdmin, InlineVideoFileAdmin
from contentcreation.services.generation import ContentGenerator
from mediacore.models import ImageFile


@admin.register(PostTag)
class PostTagAdmin(admin.ModelAdmin):
    readonly_fields = ('related_posts_amount',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(PostDelay)
class PostDelayAdmin(admin.ModelAdmin):
    readonly_fields = ('post',)

    def get_related_post_link(self, obj):
        return mark_safe("<a href='{}'>{}</a>".format(obj.get_absolute_url(), obj))

    get_related_post_link.short_description = "Отложеный объект"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [InlineImageFileAdmin, InlineVideoFileAdmin]
    list_filter = (
        'tags',
        'only_for_adult',
        'for_autenticated_users',
        'status',
    )
    list_display = (
        'id',
        'pub_date',
        'status',
        'only_for_adult',
        'for_autenticated_users',
        'disable_comments',
    )
    readonly_fields = (
        'creation_date',
        'pub_date',
    )
    exclude = (
        'views',
        'likes',
    )
    filter_horizontal = ('tags',)
    change_form_template = 'posts/image_post_change_form.html'
    actions = ('make_published',)

    def response_generate_image(self, request, post) -> bool:
        if "generate_image" in request.POST:
            try:
                cg = ContentGenerator()
                image_file = ImageFile(file=cg.generate(), post=post)
                image_file.save()
            except IndexError:
                self.message_user(request, "Ошибка генерации медиа! Список '{}' пуст.".format(cg.last_source_type), level=messages.ERROR)
            except Exception as e:
                self.message_user(request, e, level=messages.ERROR)
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
        if change and 'status' in form.changed_data:
            if post.status == Post.STATUS.PUBLISHED:
                post.pub_date = timezone.now()
            post.save(update_fields=['status', 'pub_date'])
        else:
            super().save_model(request, post, form, change)

    @admin.action(description="Опубликовать")
    def make_published(self, request, queryset):
        for post in queryset:
            if post.status == Post.STATUS.DEFERRED and post.delay:
                post.status = Post.STATUS.PUBLISHED
                post.pub_date = timezone.now()
                post.delay.delete()
                post.delay = None
            elif post.status == Post.STATUS.CONSIDERATION:
                post.status = Post.STATUS.PUBLISHED
                post.pub_date = timezone.now()
            else:
                post.status = Post.STATUS.PUBLISHED

            post.save(update_fields=['status'])

        messages.add_message(request, messages.SUCCESS, "Посты опубликованы")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = (
        'text',
        'author',
    )
    list_display = (
        'id',
        'author',
        'post',
        'pub_date',
    )
    readonly_fields = (
        'pub_date',
    )


@admin.register(UserView)
class UserViewAdmin(admin.ModelAdmin):
    search_fields = (
        'user__id',
        'post__id',
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
        'post_link',
    )

    def post_link(self, obj):
        return mark_safe("<a href='{}'>{}</a>".format(obj.post.get_absolute_url(), obj.post))

    post_link.short_description = "Просмотренный пост"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    readonly_fields = (
        'creation_date',
        'post_link',
    )

    def post_link(self, obj):
        return mark_safe("<a href='{}'>{}</a>".format(obj.post.get_absolute_url(), obj.post))

    post_link.short_description = "Лайкнутый пост"




