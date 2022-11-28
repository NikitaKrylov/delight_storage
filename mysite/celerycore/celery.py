import os
from mysite.settings import PUBLISH_POST_SCHEDULE
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

app = Celery("celerycore")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_and_publish_posts': {
        'task': "celerycore.tasks.publish_posts",
        'schedule': PUBLISH_POST_SCHEDULE,
    },
}


