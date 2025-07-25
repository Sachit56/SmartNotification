from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.exceptions import ObjectDoesNotExist
from .models import Notification

@shared_task(bind=True, default_retry_delay=10, max_retries=3)
def notify_users(self, preference, notification_id):
    try:
        print(f"[notify_users] Notification ID: {notification_id}, Preference: {preference}")

        notification = Notification.objects.get(id=notification_id)
        user_id = notification.user_id
        event = notification.event
        message = notification.message or f"New {event} notification."

        success = False

        if preference == 'app':
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{user_id}",
                {
                    'type': 'send.notification',
                    'message': message,
                }
            )
            success = True
            print(f"[notify_users] WebSocket message sent to user_{user_id}")

        elif preference == 'email':
            print(f"[notify_users] Email sent to user_{user_id}: {message}")
            success = True

        elif preference == 'sms':
            print(f"[notify_users] SMS sent to user_{user_id}: {message}")
            success = True

        notification.status = success
        notification.save()

    except ObjectDoesNotExist:
        print(f"[notify_users] Notification ID {notification_id} does not exist. Skipping.")
    except Exception as e:
        print(f"[notify_users] Error: {e}. Retry #{self.request.retries}")
        raise self.retry(exc=e)
