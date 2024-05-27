# cplatform/routing.py
from django.urls import re_path
from cplatform import consumers

websocket_urlpatterns = [
    re_path(r'chat/$', consumers.ChatConsumer.as_asgi()),
]
