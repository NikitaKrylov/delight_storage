from django.contrib import admin
from .models import User, ClientIP, Subscription, Complaint

admin.site.register(ClientIP)


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
    )
    readonly_fields = (
        'last_login',
        'is_adult',
        'subscribers_amount',
    )
    exclude = ('password',)
    filter_horizontal = ('ignored_tags',)

    def is_adult(self, obj: User):
        return obj.is_adult()

    is_adult.short_description = "18+ пользователь"
    is_adult.boolean = True

    def subscribers_amount(self, obj: User):
        return obj.user_subscriptions.count()

    subscribers_amount.short_description = "Кол-во подписчиков"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    readonly_fields = ('start_date', '_sub_time_delta',)
    list_filter = ('subscriber', 'subscription_object', 'status',)

    def _sub_time_delta(self, obj):
        return obj.sub_time_delta

    _sub_time_delta.short_description = 'Общая продолжительность подпики'


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'status',
        'recipient',
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

    @admin.action(description="Принять")
    def make_accepted(self, request, queryset):
        queryset.update(status=Complaint.Status.ACCEPTED)

    @admin.action(description="Отклонить")
    def make_rejected(self, request, queryset):
        queryset.update(status=Complaint.Status.REJECTED)

