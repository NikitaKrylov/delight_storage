from django.contrib import admin
from django.contrib import messages

from .models import *


@admin.register(TelegramChanelSource)
class TelegramChanelSourceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'use_in_generation',
    )
    actions = (
        'make_enable',
        'make_unable'
    )

    @admin.action(description="Использовать в генерации")
    def make_enable(self, request, queryset):
        queryset.update(use_in_generation=True)
        messages.add_message(request, messages.SUCCESS, "Каналы  обновлены")

    @admin.action(description="Не использовать в генерации")
    def make_unable(self, request, queryset):
        queryset.update(use_in_generation=False)
        messages.add_message(request, messages.SUCCESS, "Каналы сняты с использования")

