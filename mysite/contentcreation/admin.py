from django.contrib import admin
from .models import *


@admin.register(TelegramChanelSource)
class TelegramChanelSourceAdmin(admin.ModelAdmin):
    list_display = ('name',)