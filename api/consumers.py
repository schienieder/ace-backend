import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Chat


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        # FIND ROOM
        room = await database_sync_to_async(ChatRoom.objects.get)(
            room_name=self.room_name
        )
        # SAVE CHAT MESSAGES
        chat = Chat(content=message, room=room, user=username)
        await database_sync_to_async(chat.save)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message, "username": username},
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(
            text_data=json.dumps(
                {"type": "chat", "message": message, "username": username}
            )
        )
