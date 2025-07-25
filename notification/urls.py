from django.urls import path
from .views import *


urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('threads/',ThreadView.as_view(),name='threads'),
    path('thread-subscription/',ThreadSubscriptionView.as_view(),name='subscriptions'),
    path('preferences/',NotificationPreferenceView.as_view(),name='preferences'),
    path('unread/',UnreadNotificationView.as_view(),name='unread'),
    path('read/',ReadNotificationView.as_view(),name='read'),
    path('history/',NotificationHistoryView.as_view(),name='history'),
    path('comments/<int:thread_id>/',CommentView.as_view(),name='comment'),
    path('report/<int:thread_id>/',WeeklyReportView.as_view(),name='report'),
    path('trigger/<int:thread_id>/',CommentView.as_view(),name='trigger'),


    path('thread-socket/',thread_websocket_view,name='web')
]