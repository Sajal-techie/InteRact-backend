import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from user_auth.models import CustomUser
from .models import Chat
from .serializers import ChatSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["thread_name"]
        self.room_group_name = f"{self.room_name}"
        print('connected',self.room_name,self.room_group_name)
        # Join the chat group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        print("disconnect")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        message = data['message']
        receiver_id = data['receiver']
        sender_id = data["sender"]

        sender =  await self.get_user(sender_id)
        receiver = await self.get_user(receiver_id)
        if sender and receiver:
            
            chat = await self.save_message(message, sender, receiver, self.room_name)

            serialized_data =  await self.serialize_chat(chat)
            print(serialized_data.get('sender'), 'se-=-=-=-=-=-=-=-=-=-=-=-=')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': "chat_message",
                "message": message,
                "sender" : str(sender_id), 
                "receiver": str(receiver_id)
            }
        )
    
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        receiver = event["receiver"]

        await self.send(text_data=json.dumps({
            'message': message,
            'sender':sender,
            'receiver':receiver
        }))

    @database_sync_to_async
    def save_message(self, message, sender, receiver, thread_name):
        return Chat.objects.create(receiver=receiver, message=message, sender=sender, thread_name=thread_name)


    @database_sync_to_async
    def get_user(self, id):
        return CustomUser.objects.get(id=id)
    
    @database_sync_to_async
    def serialize_chat(self, chat):
        return ChatSerializer(chat).data