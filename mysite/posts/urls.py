from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *
from .api_views import *

router = DefaultRouter()
router.register("api/posts", PostViewSet, basename='posts')
router.register("api/tags", PostTagViewSet, basename='tags')
print(router.urls)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('posts/all/', PostList.as_view(), name='post_list'),
    path('posts/search/', SearchPostList.as_view(), name='search'),
    path('posts/search/<slug:slug>/', SearchPostTagListView.as_view(), name='search_by_tag'),
    path('posts/complication/', PostCompilationsList.as_view(), name='complication'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post'),
    path('post/<int:pk>/delete/', delete_post, name='delete_post'),

    path('post/<int:pk>/comments/add/', create_post_comment, name='add_comment'),
    path('post/comments/delete/<int:pk>/', delete_comment, name='delete_comment'),
    path('post/<int:pk>/comments/reply/add/<int:reply_comment_pk>/', create_reply_post_comment, name='add_reply_comment'),

    path('post/<int:pk>/complaint/create', create_post_complain, name='create_post_complaint'),

    path('post/<int:pk>/like/', like_post, name='post_like'),

    # path('get_tags/', get_tags, name='get_tags'),
    path('create_tag/', create_post_tag, name='create_post_tag'),

]

urlpatterns += router.urls
