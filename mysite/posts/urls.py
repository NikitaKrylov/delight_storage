from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('posts/all/', PostList.as_view(), name='post_list'),
    path('posts/search/', SearchPostList.as_view(), name='search'),
    path('posts/complication/', PostCompilationList.as_view(), name='complication'),
    path('posts/liked/', LikedPostList.as_view(), name='liked_posts'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    path('post/<int:pk>/add_comment/', AddComment.as_view(), name='add_comment'),
    path('post/<int:pk>/add_reply_comment/<int:reply_comment_pk>/', AddReplyComment.as_view(), name='add_reply_comment'),
    path('post/<int:pk>/like/', LikePostView.as_view(), name='post_like'),
]
