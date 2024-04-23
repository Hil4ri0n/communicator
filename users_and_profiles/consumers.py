from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
from django.core.cache import cache
from .models import Profile


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    @staticmethod
    def get_user_profile(user):
        return Profile.objects.get(user=user)

    def update_profile_status(self, is_online):
        profile = self.my_profile
        profile.online = is_online
        profile.save()

    async def connect(self):
        my_user = self.scope['user']
        self.my_profile = await database_sync_to_async(
            self.get_user_profile
        )(my_user)
        cache.set(f"profile_{self.my_profile.id}_connected", True, timeout=30)
        await self.channel_layer.group_add(
            'onlineStatus',
            self.channel_name
        )

        await database_sync_to_async(
            self.update_profile_status
        )(True)

        await self.channel_layer.group_send(
            'onlineStatus',
            {
                "type": "user_online",
                "action": "status_update",
                "profile_id": self.my_profile.id,
                "isOnline": True
            }
        )
        await self.accept()

    async def disconnect(self, close_code):
        cache.set(f"profile_{self.my_profile.id}_connected", False, timeout=30)
        await asyncio.sleep(3)
        if cache.get(f"profile_{self.my_profile.id}_connected"):
            return
        await database_sync_to_async(
            self.update_profile_status
        )(False)
        await self.channel_layer.group_send(
            'onlineStatus',
            {
                "type": "user_online",
                "action": "status_update",
                "profile_id": self.my_profile.id,
                "isOnline": False
            }
        )
        self.channel_layer.group_discard(
            'onlineStatus',
            self.channel_name
        )

    async def user_online(self, event):
        await self.send(text_data=json.dumps(event))
