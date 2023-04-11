from typing import List
import numpy as np
from posts.models import Post
from accounts.services.base import get_client_ip
from accounts.models import ClientIP


def update_post_views(request, post: Post):
    user = request.user

    if user.is_authenticated:
        user_view, created = post.views.get_or_create(user=user)
    else:
        clien_ip, ip_created = ClientIP.objects.get_or_create(ip=get_client_ip(request))
        user_view, created = post.views.get_or_create(client_ip=clien_ip)


def update_post_like(request, post: Post):
    user = request.user
    ctx = {"liked": None, "add_view": None}

    if user.is_authenticated:
        filter = {'user': user}
    else:
        client_ip, ip_created = ClientIP.objects.get_or_create(ip=get_client_ip(request))
        filter = {'client_ip': client_ip}

    like, created = post.likes.get_or_create(**filter)
    if not created:  # already liked the content
        like.delete()
        ctx['liked'] = False
    else:
        post.likes.add(like)
        _, created = post.views.get_or_create(**filter)
        ctx['liked'] = True
        ctx['add_view'] = created

    return ctx


