from rest_framework import generics
from .serializers import ChatSerializer
from .models import Chat

class ChatListView(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get_queryset(self):
        current = self.request.query_params.get('current')
        other = self.request.query_params.get('other')
        thread = "_".join(sorted((other,current)))
        return  Chat.objects.filter(thread_name=thread)
        
