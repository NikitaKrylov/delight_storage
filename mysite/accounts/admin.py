from django.contrib import admin
from .models import User, ContentAuthor, ClientIP

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
    )

    def is_adult(self, obj: User):
        return obj.is_adult()
    
    is_adult.boolean = True

@admin.register(ContentAuthor)
class ContentAuthorAdmin(admin.ModelAdmin):
    search_fields = [
        'name'
    ]
