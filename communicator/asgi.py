"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

"""import os

from django.core.asgi import get_asgi_application

from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter

from channels.auth import AuthMiddlewareStack

from chat.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whatsapp_clone.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/chat/<int:friend_id>/', ChatConsumer.as_asgi()),
        ])
    )
})"""

import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import chat_ws_urlpatterns  # Import the websocket routes
from users_and_profiles.routing import websocket_urlpatterns as users_ws_urlpatters

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

django_asgi_app = get_asgi_application()

combined_websocket_urlpatterns = chat_ws_urlpatterns + users_ws_urlpatters

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Use Django's ASGI application to handle HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            combined_websocket_urlpatterns  # Use the imported websocket routes
        )
    ),
})
