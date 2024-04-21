# creating routing for the consumers (see: consumers.py)
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chatroom_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]