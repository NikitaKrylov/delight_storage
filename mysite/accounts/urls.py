from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', AuthenticationView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('notifications/', NotificationListView.as_view(), name='user_notifications'),
    path('<int:pk>/profile/', UserProfileView.as_view(), name='profile'),
    path('<int:pk>/liked/', UserProfileView.as_view(), name='user_liked_posts'),
    path('<int:user_id>/subscribe-to/<int:object_id>/', Signatory.as_view(), name='subscribe'),

    # Ввод почты для отправки письма
    path('password/reset/', UserPasswordResetView.as_view(), name='password_reset_form'),
    # Сообщение об отправке ссылки на изменение пароля
    path('password/reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    # Ввод нового пароля
    path('password/reset/<str:uidb64>/<str:token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # Сообщение об успешном изменении пароля
    path('password/reset/complete', UserPasswordResetCompleteView.as_view(), name='password_reset_complete')



]


