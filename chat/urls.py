from django.urls import path
from .views import chat

urlpatterns = [
    path('<int:friend_id>/', chat, name='chat'),
]
