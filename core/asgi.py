import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from school.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/<int:course_id>/', ChatConsumer.as_asgi()),
            path('ws/chat/private/', ChatConsumer.as_asgi()),
        ])
    ),
})
