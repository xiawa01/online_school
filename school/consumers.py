import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage, Course, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.course_id = self.scope['url_route']['kwargs'].get('course_id')
        self.user = self.scope['user']
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        if self.course_id:
            self.room_group_name = f'course_{self.course_id}'
        else:
            self.room_group_name = f'user_{self.user.id}'
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'message')
        
        if message_type == 'message':
            await self.save_message(data['message'], data.get('recipient_id'))
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': data['message'],
                    'sender': self.user.username,
                    'sender_id': self.user.id,
                    'timestamp': str(data.get('timestamp'))
                }
            )
        elif message_type == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'sender': self.user.username,
                    'is_typing': data.get('is_typing', True)
                }
            )
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender': event['sender'],
            'sender_id': event['sender_id'],
            'timestamp': event['timestamp']
        }))
    
    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'sender': event['sender'],
            'is_typing': event['is_typing']
        }))
    
    @database_sync_to_async
    def save_message(self, message, recipient_id=None):
        return ChatMessage.objects.create(
            course_id=self.course_id if self.course_id else None,
            sender=self.user,
            message=message,
            is_private=bool(recipient_id),
            recipient_id=recipient_id
        )
