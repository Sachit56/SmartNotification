from django.urls import re_path
from .consumers import ThreadConsumer

websocket_patterns = [
    re_path(r'ws/notifications/$',ThreadConsumer.as_asgi()),
]