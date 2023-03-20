from typing import List, Union
import numpy as np
from django.db.models import QuerySet
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


class TagsVectorizer:
    _dimension: int = 100

    def __init__(self, dimension: int = 100):
        self._dimension = dimension

    def _from_list(self, values: List[int]) -> np.ndarray:
        vector = np.zeros(self._dimension)
        for i in values:
            vector[i-1] = i

        return vector

    def _from_post(self, post: Post) -> np.ndarray:
        return self._from_list(post.tags.values_list('id', flat=True))

    def _from_queryset(self, queryset: QuerySet[Post]) -> np.ndarray:
        return np.array([self._from_post(i) for i in queryset])

    def create(self, obj: Union[Post, List[int], QuerySet[Post]]) -> np.ndarray:
        if isinstance(obj, Post): return self._from_post(obj)

        elif isinstance(obj, QuerySet[Post]): return self._from_queryset(obj)

        elif isinstance(obj, list): return self._from_list(obj)

        raise TypeError("Type '{}' not supported".format(type(obj)))
