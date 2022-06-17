import json
from django.contrib import messages
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from channels.exceptions import StopConsumer

User = get_user_model()

class GameRoom(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' %  self.room_name
        print(self.room_group_name) 
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('receive', event)
        received_data = json.loads(event['text'])
        print(received_data)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'run_game',
                'text' : json.dumps(received_data)
            }
        )

    async def run_game(self, event):
        # print('run_game', event)

        await self.send({
            'type' : 'websocket.send',
            'text': event['text']
        })   



    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print('disconnect', event)
        raise StopConsumer()
        
         