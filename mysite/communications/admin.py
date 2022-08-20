from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_filter = (
        'type',
        'status',
    )
    readonly_fields = (
        'creation_date',
    )
    list_display = (
        'author',
        'type',
        'status',
        'creation_date',
    )
