# creating a consumer to handle WebSocket connections and message sending or receiving
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']
        self.chatroom_group_name = f'chat_{self.chatroom_id}'

        # Join chatroom group
        await self.channel_layer.group_add(
            self.chatroom_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave chatroom group
        await self.channel_layer.group_discard(
            self.chatroom_group_name,
            self.channel_name
        )

        

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        message = data_json['message']
        sender_id = self.scope['user'].id

        # Save message to database
        await self.save_message(message)

        # Broadcast message to chatroom group
        await self.channel_layer.group_send(
            self.chatroom_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']  # Assuming you pass the sender's ID along with the event
        sender_username = await self.get_sender_username(sender_id)  # Get the sender's username
        await self.send(text_data=json.dumps({
            'username': sender_username,
            'message': message
        }))


    async def save_message(self, message):
        sender_id = self.scope['user'].id  # Assuming you're saving the sender's ID
        # Save message to database asynchronously
        await sync_to_async(Message.objects.create)(
            chatroom_id=self.chatroom_id,
            sender_id=sender_id,
            content=message
        )

    async def get_sender_username(self, sender_id):
        sender = await sync_to_async(User.objects.get)(id=sender_id)
        return sender.username