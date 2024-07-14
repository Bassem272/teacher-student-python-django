
# chat/consumers.py
import datetime
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
    def receive(self, text_data):
        try:
            time = datetime.datetime.now(datetime.timezone.utc).isoformat()
            text_data_json = json.loads(text_data)
            if text_data_json["type"] == "joined":
                print(f"we received a join >> receive_consumer_up>>>>>> {time} ________________>>>>>>>>>>>", text_data_json)
                content = text_data_json.get("content")
                grade = text_data_json.get("grade")
                id = text_data_json.get("id")
                time = text_data_json.get("time")
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                    "type": "chat.message",
                    "message": text_data_json
                    }
                    )
                print(f'we sent a message to the rooms now lol! << receive_consumer_down >>>>>>>>> {time}____________>>>>>>>>')
            if text_data_json["type"] == "message":
                print(f"we received a<< type:  message now >> receive_consumer_up>>>>>> {time} ________________>>>>>>>>>>>", text_data_json)
                content = text_data_json.get("content")
                grade = text_data_json.get("grade")
                id = text_data_json.get("id")
                time = text_data_json.get("time")
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                    "type": "chat.message",
                    "message": text_data_json
                    }
                    )
                print(f'we sent a message to the rooms now lol!<< type : message  << receive_consumer_down >>>>>>>>> {time}____________>>>>>>>>')
            if text_data_json["type"] == "file":
                print(f"we received a<< type:  file now >> receive_consumer_up>>>>>> {time} ________________>>>>>>>>>>>", text_data_json)
                content = text_data_json.get("content")
                grade = text_data_json.get("grade")
                id = text_data_json.get("id")
                time = text_data_json.get("time")
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                    "type": "chat.message",
                    "message": text_data_json
                    }
                    )
                print(f'we sent a message to the rooms now lol!<< type : message  << receive_consumer_down >>>>>>>>> {time}____________>>>>>>>>')
       
        except Exception as e:
            print(e)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat.message",
                    "message": f"error: {str(e)}"
                }
            )
    # Receive message from room group
    def chat_message(self, event):
        print('event is :',event)
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))