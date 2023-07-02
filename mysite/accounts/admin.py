from django.contrib import admin

from mysite.errors import IncorrectDeletionError
from .models import User, ClientIP, Subscription, PostComplaint, Folder, FolderPost, Role, UserSettings

admin.site.register(ClientIP)
admin.site.register(Role)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = (
        'username',
        'email',
    )
    list_display = (
        'username',
        'email',
        'is_adult',
        'role',
    )
    readonly_fields = (
        'last_login',
        'is_adult',
        'subscribers_amount',
    )
    exclude = ('password',)

    def is_adult(self, obj: User):
        return obj.is_adult()

    is_adult.short_description = "18+ пользователь"
    is_adult.boolean = True

    def subscribers_amount(self, obj: User):
        return obj.user_subscriptions.count()

    subscribers_amount.short_description = "Кол-во подписчиков"


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user',)

    def delete_model(self, request, obj):
        raise IncorrectDeletionError("You cannot delete \"UserSettings\" model manually, deletion is possible by cascading deletion through the user model")

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'user',
        'created',
    )
    readonly_fields = ('created',)


@admin.register(FolderPost)
class FolderPostAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'folder',
        'created',
    )
    readonly_fields = ('created',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = ('start_date', '_sub_time_delta',)
    list_filter = ('subscriber', 'subscription_object', 'status',)

    def _sub_time_delta(self, obj):
        return obj.sub_time_delta

    _sub_time_delta.short_description = 'Общая продолжительность подпики'


@admin.register(PostComplaint)
class PostComplaintAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'status',
        'sender',
        'post',
        'creation_date',
    )
    list_filter = (
        'status',
        'type',
    )
    actions = (
        'make_accepted',
        'make_rejected',
    )
    readonly_fields = (
        'post',
        'creation_date',
    )

    @admin.action(description="Принять")
    def make_accepted(self, request, queryset):
        queryset.update(status=PostComplaint.Status.ACCEPTED)

    @admin.action(description="Отклонить")
    def make_rejected(self, request, queryset):
        queryset.update(status=PostComplaint.Status.REJECTED)

