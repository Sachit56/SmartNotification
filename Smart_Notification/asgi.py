"""
ASGI config for Smart_Notification project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os,django

from django.core.asgi import get_asgi_application
from channels.routing import URLRouter,ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from notification.routing import websocket_patterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Smart_Notification.settings')


application = ProtocolTypeRouter({
    "http":get_asgi_application(),
    "websocket":AuthMiddlewareStack(URLRouter(websocket_patterns))
})
