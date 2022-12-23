from .models import User
from posts.models import Comment, Like, UserView, Post
from django.db.models import Count, Sum


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def count_posts_elements(user: User, field: str):
    return Post.objects.filter(author=user).aggregate(value=Count(field))['value']


def best_post(user: User, field: str):
    return Post.objects.filter(author=user).annotate(value=Sum(field))


