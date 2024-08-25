from django.db import models
from user_auth.models import CustomUser
class Chat(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='send_message')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receive_message')
    message = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    thread_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"chat instance {self.sender.username} - {self.receiver.username} - {self.message}"