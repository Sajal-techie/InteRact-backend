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
        if data.get('type') == 'video-call-invite':
            print(f"Received video call invite: {data}")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'video_call_invite',
                    'roomId': data['roomId'],
                    'sender': data['sender'],
                    'receiver': data['receiver'],
                    'message': data['message'],
                }
            )
        else:
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

    async def video_call_invite(self, event):
        print(f"Sending video call invite: {event}")
        await self.send(text_data=json.dumps({
            'type': 'video-call-invite',
            'roomId': event['roomId'],
            'sender': event['sender'],
            'receiver': event['receiver'],
            'message': event['message'],
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
    

class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'video_{self.room_name}'
        print(f'Video consumer connecting to room: {self.room_name}')
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f'Video consumer connected to room: {self.room_name}')

    async def disconnect(self, close_code):
        print(f'Video consumer disconnecting from room: {self.room_name}')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data['type']
        print(f"Video consumer received message type: {message_type}")
        if message_type in ['offer', 'answer', 'ice-candidate','ready', 'end-call']:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'signal',
                    'message': data,
                }
            )

    async def signal(self, event):
        print(f"Video consumer signaling: {event['message']['type']}")
        message = event['message']
        await self.send(text_data=json.dumps(message))


class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = 'presence'
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        
        await self.set_user_online(self.user_id)
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "user_online", "user_id": self.user_id}
        )

    async def disconnect(self, close_code):
        await self.set_user_offline(self.user_id)
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "user_offline", "user_id": self.user_id}
        )
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def user_online(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_offline(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def set_user_online(self, user_id):
        CustomUser.objects.filter(id=user_id).update(is_online=True)

    @database_sync_to_async
    def set_user_offline(self, user_id):
        CustomUser.objects.filter(id=user_id).update(is_online=False)