from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', AuthenticationView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    path('user/profile/', UserProfileView.as_view(), name='profile'),
    path('user/profile/edit/', edit_user_form, name='profile_edit'),

    path('user/self-posts/', UserPostListView.as_view(), name='self_user_posts'),
    path('user/self-posts/create/', CreatePostView.as_view(), name='create_post'),
    path('user/self-posts/change/<int:pk>/',
         EditPostView.as_view(), name='change_post'),

    path('user/settings/', UserSettingsFormView.as_view(), name='user_settings'),
    path('user/settings/edit/', edit_user_settings, name='user_settings_edit'),

    path('user/notifications/', UserNotificationListView.as_view(),
         name='user_notifications'),
    path('user/notification/<int:pk>/delete/', delete_notification, name='notification_delete'),
    path('user/notification/<int:pk>/read/', read_notification, name='notification_read'),
    path('user/notifications/all/delete/', delete_all_notification, name='all_notification_delete'),
    path('user/notifications/all/read/', read_all_notification, name='all_notification_read'),

    path('user/subscriptions/', UserSubscriptionListView.as_view(),
         name='user_subscriptions'),
    path('user/subscribe-to/<int:object_id>/',
         Signatory.as_view(), name='subscribe'),

    path('user/likes/', LikedPostList.as_view(), name='user_liked_posts'),

    path('user/dashboard/', UserDashBoard.as_view(), name='dashboard'),


    # Ввод почты для отправки письма
    path('password/reset/', UserPasswordResetView.as_view(),
         name='password_reset_form'),
    # Сообщение об отправке ссылки на изменение пароля
    path('password/reset/done/', UserPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    # Ввод нового пароля
    path('password/reset/<str:uidb64>/<str:token>/',
         UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # Сообщение об успешном изменении пароля
    path('password/reset/complete', UserPasswordResetCompleteView.as_view(),
         name='password_reset_complete')

]
