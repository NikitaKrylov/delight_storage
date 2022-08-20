from django.urls import path
from .views import RegisterView, AuthenticationView, UserProfileView

urlpatterns = [
    path('logout/', RegisterView.as_view(), name='logout'),
    path('login/', AuthenticationView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile')

]
