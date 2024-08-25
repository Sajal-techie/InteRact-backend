from rest_framework import serializers
from user_auth.serializers import CustomUserSerializer
from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    # sender = CustomUserSerializer(read_only=True)


    class Meta:
        model = Chat
        fields = ['id', 'sender', 'receiver', 'date', 'thread_name','message']