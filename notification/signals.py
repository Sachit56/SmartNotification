from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ThreadSubscription,Comment
from .utils import save_queue_notification


@receiver(post_save, sender = ThreadSubscription)
def subscribe_notification(sender, instance, created, **kwargs):
    if not created:
        return

    thread = instance.threads
    user = instance.user
    message = f'A new user ({user}) subscribed the thread ({thread})'

    other_subscribers = ThreadSubscription.objects.filter(threads=thread).exclude(user=user)


    for subscriber in other_subscribers:
        notification = save_queue_notification(subscriber,message,'subscribe')

        if notification:
            print(f'Notification saved of User ({user}).')


@receiver(post_save, sender=Comment)
def comment_notification(sender,instance,created, **kwargs):
    if not created:
        return
    
    thread = instance.thread
    user = instance.user
    message = f'User ({user}) commented on a thread({thread}).'

    other_subscribers = ThreadSubscription.objects.filter(threads=thread).exclude(user=user)

    for subscriber in other_subscribers:
        notification = save_queue_notification(subscriber,message,'comment')

        if notification:
            print(f'Notification saved of User ({user}).')