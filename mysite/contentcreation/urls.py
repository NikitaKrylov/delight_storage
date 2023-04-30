from django.urls import path
from .views import *

urlpatterns = [
    path('parse/', get_parsered_image_path, name='get_parseed_image_path'),
    path('delete/', get_parsered_image_path, name='delete_parseed_image'),
]