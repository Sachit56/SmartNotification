import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smart_Notification.settings')

app = Celery('Smart_Notification')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()