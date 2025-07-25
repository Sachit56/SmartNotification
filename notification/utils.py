
from .models import Notification,NotificationPreference
from django.db import transaction
from .tasks import notify_users


def save_queue_notification(subscriber,message,event):

    username = subscriber.user

    notification = Notification.objects.create(
        user = username,
        message = message,
        event = event
    )

    try:
        preference = NotificationPreference.objects.get(user=username).preference
    except NotificationPreference.DoesNotExist:
        preference = 'app'

    def enqueue_task():
        notify_users.delay(preference,notification.id)

    transaction.on_commit(enqueue_task)
    
    return notification


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

def get_user_agent(request):
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    return user_agent