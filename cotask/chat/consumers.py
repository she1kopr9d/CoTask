import json

import channels.db
import channels.generic.websocket

import django.contrib.auth.models

import chat.models


class ChatConsumer(channels.generic.websocket.AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_group_name = f"chat_{self.chat_id}"

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        sender_id = self.scope["user"].id

        await self.save_message(sender_id, self.chat_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": self.scope["user"].username,
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "sender": event["sender"],
                }
            )
        )

    @channels.db.database_sync_to_async
    def save_message(self, sender_id, chat_id, message):
        sender = django.contrib.auth.models.User.objects.get(id=sender_id)
        chat_obj = chat.models.Chat.objects.get(id=chat_id)
        return chat.models.Message.objects.create(
            chat=chat_obj, sender=sender, text=message
        )
