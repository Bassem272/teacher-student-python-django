# //////

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chat_room'
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print('bassem connected here >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('bassem connected here >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # message = text_data_json['message']



        print(text_data_json)
        # message = text_data_json['message']


        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat.message',
        #         'message': message
        #     }
        # )

    # async def chat_message(self, event):
    #     message = event['message']

    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))
