from collections import defaultdict
from dataclasses import dataclass
from typing import List, Union, Set
import numpy as np
import pandas as pd
from django.db.models import QuerySet
from posts.models import Post
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import jaccard_score


def create_distance_matrix(posts):
    l = len(posts)
    matrix = np.zeros((l, l))
    posts_tags = TagsVectorizer().create(posts)

    for i in range(l):
        for j in range(l):
            matrix[i, j] = 1 - jaccard_score(posts_tags[i], posts_tags[j], average='macro')

    return matrix


@dataclass(frozen=True)
class PostCluster:
    label: int
    queryset: QuerySet[Post]

    def __len__(self):
        return self.queryset.count()


class TagsVectorizer:
    _dimension: int = 100

    def __init__(self, dimension: int = 100):
        self._dimension = dimension

    def _from_list(self, values: List[int], ones_value=False) -> np.ndarray:
        vector = np.zeros(self._dimension, dtype=np.int64)
        for i in values:
            vector[i-1] = 1 if ones_value else i

        return vector

    def _from_post(self, post: Post, ones_value=False) -> np.ndarray:
        return self._from_list(post.tags.values_list('id', flat=True), ones_value)

    def _from_queryset(self, queryset: QuerySet[Post], ones_value=False) -> np.ndarray:
        return np.array([self._from_post(i, ones_value) for i in queryset])

    def create(self, obj: Union[Post, List[int], QuerySet[Post]], ones_value=False) -> np.ndarray:
        if isinstance(obj, Post): return self._from_post(obj, ones_value)

        elif isinstance(obj, QuerySet[Post]): return self._from_queryset(obj, ones_value)

        elif isinstance(obj, list): return self._from_list(obj, ones_value)

        raise TypeError("Type '{}' not supported".format(type(obj)))


class PostClustering(AgglomerativeClustering):
    distance_matrix: np.ndarray
    dataset: pd.DataFrame

    def __init__(self, distance_threshold: int = 0.8, ):
        super(PostClustering, self).__init__(affinity='precomputed', linkage='complete', distance_threshold=distance_threshold, n_clusters=None, compute_full_tree=True)

    def fit(self, queryset: QuerySet[Post], mis_cluster_size: int = 3):
        queryset = queryset.order_by('id')
        posts_id = queryset.values_list('id', flat=True)
        self.distance_matrix = create_distance_matrix(queryset)
        self.dataset = pd.DataFrame(self.distance_matrix, columns=posts_id, index=posts_id)

        super().fit(self.dataset.values)

        clusters = defaultdict(set)
        for post, i in zip(list(queryset), self.labels_):
            clusters[i].add(post.id)

        return filter(lambda c: len(c) >= mis_cluster_size, set(PostCluster(label, Post.objects.filter(id__in=ids).all()) for label, ids in clusters.items()))




