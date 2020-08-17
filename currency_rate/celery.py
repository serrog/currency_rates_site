import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "currency_rate.settings")

app = Celery("currency_rate")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
