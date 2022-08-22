from django.urls import path
from .views import RegisterView, AuthenticationView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', AuthenticationView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile')

]
