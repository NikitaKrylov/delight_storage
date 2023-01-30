from django.contrib.auth import get_user_model
from django.db.models import Count
from django.test import TestCase
from posts.models import Post, UserView, Like
from random import randint


class PostTestCase(TestCase):
    def setUp(self):
        user = get_user_model().objects.first()

        for post in Post.objects.bulk_create((Post(author=user) for i in range(50))):
            Like.objects.bulk_create((Like(post=post, user=user) for i in range(randint(0, 30))))
            UserView.objects.bulk_create((UserView(post=post, user=user) for i in range(randint(0, 30))))

    def test_like_and_views_annotation_is_correct(self):
        posts = Post.objects.annotate(
            views_amount=Count('views', distinct=True),
            likes_amount=Count('likes', distinct=True)
        )

        for post in posts.all():
            self.assertEqual(post.views.count(), post.views_amount)
            self.assertEqual(post.likes.count(), post.likes_amount)


