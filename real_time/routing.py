from django.urls import path
from .consumers import ChatConsumer

websocket_urlpattens = [
    path('ws/chat/<str:thread_name>/', ChatConsumer.as_asgi()),
]