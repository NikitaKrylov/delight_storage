
from django.urls import path
from .views import PostView, PostList, LikePostView


urlpatterns = [
    path('post/all/', PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    path('post/id<int:pk>/like/', LikePostView.as_view(), name='post_like'),
]
