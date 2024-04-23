import asyncio
import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from users_and_profiles.models import Profile


class ChatConsumer(AsyncWebsocketConsumer):


    @staticmethod
    def get_user_profile(user):
        return Profile.objects.get(user=user)

    @staticmethod
    def get_chat_room(profile_id, friend_id):
        chat_room = ChatRoom.objects.filter(participants__id=profile_id) \
            .filter(participants__id=friend_id).first()
        return chat_room, chat_room.id

    async def connect(self):
        my_user = self.scope['user']
        self.my_profile = await database_sync_to_async(
            self.get_user_profile
        )(my_user)
        friend_id = self.scope['url_route']['kwargs']['friend_id']
        chat_room, chat_room_id = await database_sync_to_async(
            self.get_chat_room
        )(self.my_profile.id, friend_id)
        self.chat_room_id = chat_room_id
        self.room_group_name = 'chat_%s' % self.chat_room_id

        # send viewed message
        content = {
            'action': 'viewed',
            'sender_id': friend_id,
        }

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'content': content,
            },
        )

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """when user leaves chat but has something written inside input,
            the 'Typing...' message should disappear"""
        content = {
                'type': 'chat_message',
                'action': 'typing',
                'state': False,
                'sender_id': self.my_profile.id,
            }
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'content': content,
            },
        )
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        if action == 'message':
            message = text_data_json['message']
            sender_id = text_data_json['sender_id']
            print(self.my_profile.nickname, ': ', message)

            await self.save_message(message, sender_id)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'content': text_data_json
                }
            )
        elif action == 'typing' or action == 'viewed':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'content': text_data_json
                }
            )

    @database_sync_to_async
    def save_message(self, message, profile_id):
        sender_profile_obj = Profile.objects.get(id=profile_id)
        chat_room = ChatRoom.objects.get(id=self.chat_room_id)
        message_obj = Message.objects.create(chat_room=chat_room,
                                             sender=sender_profile_obj, content=message)

    async def chat_message(self, event):
        text_data = event['content']
        await self.send(text_data=json.dumps(text_data))



