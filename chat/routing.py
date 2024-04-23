from django.urls import path
from .consumers import ChatConsumer

chat_ws_urlpatterns = [
    path('ws/chat/<int:friend_id>/', ChatConsumer.as_asgi()),
]
