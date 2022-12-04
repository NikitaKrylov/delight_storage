from django.contrib import admin
from .models import User, ClientIP

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
        'id',
        'last_login',
        'is_adult',
    )
    exclude = ('password',)
    filter_horizontal = ('ignored_tags',)

    def is_adult(self, obj: User):
        return obj.is_adult()

    is_adult.short_description = "18+ пользователь"
    
    is_adult.boolean = True
