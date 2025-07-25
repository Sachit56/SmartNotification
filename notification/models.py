from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserLoginRecord(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    user_agent = models.TextField(blank=True)
    last_login = models.DateField(auto_now_add=True)



class Threads(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='threads')
    title = models.CharField(max_length=100,unique=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ThreadSubscription(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    threads = models.ForeignKey(Threads,on_delete=models.CASCADE,related_name='subscriptions')
    subscribed_at = models.DateField(auto_now_add=True)


class Comment(models.Model):
    thread = models.ForeignKey(Threads,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)

class Notification(models.Model):
    event_choice = (
    ('comment','Comment'),
    ('login','Login'),
    ('subscribe','Subscribe'),
    ('report','Report')
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    event = models.CharField(choices=event_choice,default='post')
    status = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

class NotificationPreference(models.Model):
    notify_choice = (
    ('app','App'),
    ('email','Email'),
    ('sms','SMS')
    )

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    preference = models.CharField(choices=notify_choice,default='email')

