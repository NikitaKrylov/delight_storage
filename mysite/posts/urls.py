from django.urls import path
from .views import PostView, PostList, LikePostView, HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('posts/all/', PostList.as_view(), name='post_list'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    path('post/id<int:pk>/like/', LikePostView.as_view(), name='post_like'),
]
