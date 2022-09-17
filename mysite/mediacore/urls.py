from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


urlpatterns = [
    path('hent/', IndexImg.as_view(), name='hent'),
]
