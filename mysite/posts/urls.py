
from django.urls import path
from .views import ImagePostView, VideoPostView, TextPostView, ImagePostList, LikePostView


urlpatterns = [
    path('image-post/<int:pk>/', ImagePostView.as_view(), name='imagepost'),
    path('video-post/<int:pk>/', VideoPostView.as_view(), name='videopost'),
    path('text-post/<int:pk>/', TextPostView.as_view(), name='textpost'),

    path('image-post/<int:pk>/like', LikePostView.as_view(), name='imagepost_like'),
    path('video-post/<int:pk>/like', LikePostView.as_view(), name='videopost_like'),

    path('image-post/all/', ImagePostList.as_view(), name='image_post_list')
]
