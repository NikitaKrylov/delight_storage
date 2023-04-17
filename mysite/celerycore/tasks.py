from django.utils import timezone
from .celery import app
from posts.models import Post
from celery import shared_task


@app.task
def publish_posts():
    posts = list(Post.objects.filter(status=Post.STATUS.DEFERRED).filter(delayed_publication_time__lte=timezone.now()))

    for post in posts:
        post.status = Post.STATUS.PUBLISHED
        post.pub_date = post.delayed_publication_time
        post.delayed_publication_time = None
        post.save(update_fields=['status', 'pub_date', 'delayed_publication_time'])

    return f"Publish post, amount: {len(posts)}"


@shared_task
def parse_image_from_source():
    pass

