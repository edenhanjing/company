# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        message = {}
        message['msg'] = ''
        message['username'] = self.scope['user'].username
        message['status'] = 'logout'
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = {}
        message['msg'] = text_data_json['message']
        message['username'] = self.scope['user'].username
        message['nickname'] = text_data_json['nickname']
        message['avater_url'] = text_data_json['user_avater_url']
        try:
            message['status'] = text_data_json['status']
        except:
            pass
        #print (text_data_json)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_name_ = self.scope['url_route']['kwargs']['user_name']
        self.user_group_name = 'user_%s' % self.user_name_

        # Join room group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        await self.accept()

        message = {}
        message['msg'] = 'WebSocket链接成功!'
        await self.channel_layer.group_send(
            self.user_group_name,
            {
                'type': 'user_message',
                'message': message
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.user_group_name,
            self.channel_name
        )

    async def user_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
