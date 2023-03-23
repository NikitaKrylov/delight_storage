from django.db.models import QuerySet
from posts.models import Post, Like, PostTag
import pandas as pd
from posts.services.clustering import TagsVectorizer


def create_dataset(queryset: QuerySet[Post]):
    data = queryset.values('id', 'only_for_adult', 'for_autenticated_users')

    dataset = pd.DataFrame(data=data)
    dataset['tags'] = list(TagsVectorizer(PostTag.objects.last().id).create(queryset, True))
    dataset['only_for_adult'] = dataset['only_for_adult'].astype(int)
    dataset['for_autenticated_users'] = dataset['for_autenticated_users'].astype(int)
    dataset['like'] = 1

    return dataset


