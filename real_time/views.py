from rest_framework import generics,views,response
from .serializers import ChatSerializer
from .models import Chat
import random
import string

class ChatListView(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get_queryset(self):
        current = self.request.query_params.get('current')
        other = self.request.query_params.get('other')
        thread = "_".join(sorted((other,current)))
        return  Chat.objects.filter(thread_name=thread)
        

class CreateRoomView(views.APIView):
    def get(self, request, *args, **kwargs):
        room_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return response.Response({"room_id":room_id})