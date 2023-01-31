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
    path('', include('social_django.urls')),
]


urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = 'mysite.views.heandler404'
handler500 = 'mysite.views.heandler500'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
