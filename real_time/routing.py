from django.urls import path,re_path
from .consumers import ChatConsumer,VideoCallConsumer

websocket_urlpattens = [
    path('ws/chat/<str:thread_name>/', ChatConsumer.as_asgi()),
    path('ws/video/<str:room_name>/', VideoCallConsumer.as_asgi()),
] 