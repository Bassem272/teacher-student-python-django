# # chat/consumers.py
# import json

# from channels.generic.websocket import WebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         self.send(text_data=json.dumps({"message": message}))
       
# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        # print(self)
        # print(self.room_name)

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

    # Receive message from WebSocket
    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            if(text_data_json["type"] == "joined"):
                print("we received a join now lol!",text_data_json
            
                 ) 
                content = text_data_json["content"]
                grade = text_data_json["grade"]
                id = text_data_json["id"]
                time = text_data_json["time"]
            
            # print("we received a data now lol!",text_data_json)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                  {"type": "chat.message", 
                    "message":f' person with id {id} joined the room at {time} grade {grade} >>> the message is: {content}' })
                print('we send a message for a the rooms  in now lol!')
           
        except Exception as e:
            print(e)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "chat.message", "message": "error"})
            
    # Receive message from room group
    def chat_message(self, event):
        print('event is :',event)
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))