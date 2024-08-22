from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=255)

    USERNAME_FIELD = "email"


    def __str__(self):
        return self.username + self.email + " user instance "
    