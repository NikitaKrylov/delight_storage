from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('posts/all/', PostList.as_view(), name='post_list'),
    path('posts/search/', SearchPostList.as_view(), name='search'),
    path('posts/complication/', PostCompilationsList.as_view(), name='complication'),
    #     path('posts/liked/', LikedPostList.as_view(), name='liked_posts'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    path('post/<int:pk>/delete/', delete_post, name='delete_post'),
    path('post/<int:pk>/comments/add/', AddCommentView.as_view(), name='add_comment'),
    path('post/comments/delete/<int:pk>/', delete_comment, name='delete_comment'),
    path('post/<int:pk>/comments/reply/add/<int:reply_comment_pk>/', AddReplyCommentView.as_view(), name='add_reply_comment'),
    path('post/<int:pk>/complaint/create', CreateComplaint.as_view(), name='create_post_complaint'),
    path('post/<int:pk>/comments/add/', AddCommentView.as_view(), name='add_comment'),
    path('post/<int:pk>/comments/reply/add/<int:reply_comment_pk>/', AddReplyCommentView.as_view(), name='add_reply_comment'),
    path('post/<int:pk>/like/', LikePostView.as_view(), name='post_like'),

    path('get_tags/', get_tags, name='get_tags'),
]
