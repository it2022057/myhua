import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hua_cbms.settings")

app = Celery("hua_cbms")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
