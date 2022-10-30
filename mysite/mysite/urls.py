import notifications.urls
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path('account/', include('accounts.urls')),
    path('inbox/notifications/',
         include(notifications.urls, namespace='notifications')),
]

# handler400 = 'my_app.views.bad_request'
# handler403 = 'my_app.views.permission_denied'
# handler404 = 'my_app.views.page_not_found'
# handler500 = 'my_app.views.server_error'


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
