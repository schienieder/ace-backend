import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Chat, Account, Admin, Client, BusinessPartner


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
        content = text_data_json["content"]
        username = text_data_json["username"]

        # FIND ROOM
        room = await database_sync_to_async(ChatRoom.objects.get)(
            room_key=self.room_name
        )
        # RETRIEVE SENDER ACCOUNT
        sender_account = await database_sync_to_async(Account.objects.get)(
            username=username
        )
        global sender_name
        # RETRIEVE SENDER NAME
        if sender_account.role == "client":
            sender = await database_sync_to_async(Client.objects.get)(
                account=sender_account
            )
            sender_name = f"{sender.first_name} {sender.last_name}"
        elif sender_account.role == "partner":
            sender = await database_sync_to_async(BusinessPartner.objects.get)(
                account=sender_account
            )
            sender_name = f"{sender.first_name} {sender.last_name}"
        else:
            sender = await database_sync_to_async(Admin.objects.get)(
                account=sender_account
            )
            sender_name = f"{sender.first_name} {sender.last_name}"

        # SAVE CHAT MESSAGES
        chat = Chat(
            content=content, room=room, sender_name=sender_name, username=username
        )
        await database_sync_to_async(chat.save)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "content": content,
                "sender_name": sender_name,
                "username": username,
            },
        )

    async def chat_message(self, event):
        content = event["content"]
        sender = event["sender_name"]
        username = event["username"]
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat",
                    "content": content,
                    "sender_name": sender,
                    "username": username,
                }
            )
        )
