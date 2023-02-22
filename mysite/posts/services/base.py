from typing import List
import numpy as np
from posts.models import Post, PostTag
from accounts.services.base import get_client_ip
from accounts.models import ClientIP


def update_post_views(request, post: Post):
    if post is None: return
    user = request.user

    if user.is_authenticated:
        user_view, created = post.views.get_or_create(user=user)
    else:
        clien_ip, ip_created = ClientIP.objects.get_or_create(ip=get_client_ip(request))
        user_view, created = post.views.get_or_create(client_ip=clien_ip)


def tags_vector(tags_id: List[int], max_size: int = 100):
    vector = np.zeros(max_size)
    for i in tags_id:
        vector[i-1] = i
    return vector