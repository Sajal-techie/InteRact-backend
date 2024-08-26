from django.urls import path,re_path
from .consumers import ChatConsumer,VideoCallConsumer,PresenceConsumer

websocket_urlpattens = [
    path('ws/chat/<str:thread_name>/', ChatConsumer.as_asgi()),
    path('ws/video/<str:room_name>/', VideoCallConsumer.as_asgi()),
    path('ws/presence/<str:user_id>/', PresenceConsumer.as_asgi()),
] 