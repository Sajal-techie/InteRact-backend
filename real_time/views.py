from rest_framework import generics,views,response
from .serializers import ChatSerializer
from .models import Chat
import random
import string
from user_auth.serializers import CustomUser, UserIdSerializer

class ChatListView(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get_queryset(self):
        current = self.request.query_params.get('current')
        other = self.request.query_params.get('other')
        thread = "_".join(sorted((other,current)))
        return  Chat.objects.filter(thread_name=thread)
        

class ListOnlineUsersView(generics.ListAPIView):
    serializer_class = UserIdSerializer
    queryset = CustomUser.objects.filter(is_online=True).exclude(is_staff=True)    

    def get_queryset(self):
        print(CustomUser.objects.filter(is_online=True).exclude(is_staff=True) ,'][][[][][][][][][][values]]'   )
        return super().get_queryset()