import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

app = Celery("celerycore")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_and_publish_posts': {
        'task': "celerycore.tasks.publish_posts",
        'schedule': 5.0,
    },
}


