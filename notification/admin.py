from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(UserLoginRecord)
class UserLoginRecordAdmin(admin.ModelAdmin):
    list_display = ('user','user_agent','last_login',)
    search_fields = ('user__username__icontains',)

@admin.register(Threads)
class ThreadsAdmin(admin.ModelAdmin):
    list_display = ('title','author','created_at')
    list_filter = ('title','author')
    search_fields = ('title','author')

@admin.register(ThreadSubscription)
class ThreadSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user','threads','subscribed_at')
    search_fields = ('threads__title__icontains',)

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user','preference')
    list_filter = ('user','preference')
    search_fields = ('user__username__icontains','preference')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user','event','is_read','status','created_at')
    list_filter = ('user','event','is_read','status')
    search_fields = ('user__username__icontains','event')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','thread','created_at')
    list_filter = ('created_at','thread','user')
    search_fields = ('user__username__icontains','thread__title__icontains')