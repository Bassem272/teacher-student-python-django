# # # //////

# # import json
# # from channels.generic.websocket import AsyncWebsocketConsumer

# # class ChatConsumer(AsyncWebsocketConsumer):
# #     async def connect(self):
# #         self.room_name = 'chat_room'
# #         self.room_group_name = f'chat_{self.room_name}'

# #         await self.channel_layer.group_add(
# #             self.room_group_name,
# #             self.channel_name
# #         )
# #         print('bassem connected here >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
# #         await self.accept()

# #     async def disconnect(self, close_code):
# #         await self.channel_layer.group_discard(
# #             self.room_group_name,
# #             self.channel_name
# #         )

# #     async def receive(self, text_data):
# #         text_data_json = json.loads(text_data)
# #         print('bassem connected here >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
# #         # message = text_data_json['message']



# #         print(text_data_json)
# #         # message = text_data_json['message']


# #         # await self.channel_layer.group_send(
# #         #     self.room_group_name,
# #         #     {
# #         #         'type': 'chat.message',
# #         #         'message': message
# #         #     }
# #         # )

# #     # async def chat_message(self, event):
# #     #     message = event['message']

# #     #     await self.send(text_data=json.dumps({
# #     #         'message': message
# #     #     }))


# import datetime
# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_{self.room_name}"

#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )
#         self.accept()

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )

#     def receive(self, text_data):
#         try:
#             time = datetime.datetime.now(datetime.timezone.utc).isoformat()
#             text_data_json = json.loads(text_data)
#             message_type = text_data_json.get("type")

#             if message_type in ["joined", "message"]:
#                 async_to_sync(self.channel_layer.group_send)(
#                     self.room_group_name,
#                     {
#                         "type": "chat_message",
#                         "message": text_data_json,
#                     }
#                 )
#                 print(f"Received and forwarded message of type: {message_type}")

#         except Exception as e:
#             async_to_sync(self.channel_layer.group_send)(
#                 self.room_group_name,
#                 {
#                     "type": "chat_message",
#                     "message": {"type": "error", "content": str(e)},
#                 }
#             )

#     def chat_message(self, event):
#         message = event["message"]
#         self.send(text_data=json.dumps({"message": message}))
import datetime
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Ensure that 'room_name' is correctly captured from the URL
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        try:
            time = datetime.datetime.now(datetime.timezone.utc).isoformat()
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get("type")

            if message_type in ["joined", "message"]:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        "type": "chat_message",
                        "message": text_data_json,
                    }
                )
                print(f"Received and forwarded message of type: {message_type}")

        except Exception as e:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": {"type": "error", "content": str(e)},
                }
            )

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))
