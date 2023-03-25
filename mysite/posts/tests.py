from django.contrib.auth import get_user_model
from django.db.models import Count, ExpressionWrapper, FloatField, Case, When, Value, F, QuerySet
from django.test import TestCase
from posts.models import Post, UserView, Like, PostTag
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

    def test_like_percent_annotation(self):
        msg = "\nLikes: {} \nViews: {} \nCalculating result: {} \nExpected result: {}"
        posts = Post.objects.annotate(
            views_amount=Count('views', distinct=True),
            likes_amount=Count('likes', distinct=True)
        )
        posts = posts.annotate(
            value=Case(
                When(likes_amount=0, then=Value(0.0)),
                default=ExpressionWrapper(
                    F('likes_amount') * 1.0 / F('views_amount'), output_field=FloatField()
                )
            )
        )
        for post in posts.all():
            views = post.views.count()
            likes = post.likes.count()
            self.assertEqual(post.likes.count() / post.views.count(), post.value, msg.format(
                likes,
                views,
                post.value,
                likes / views
            ))




