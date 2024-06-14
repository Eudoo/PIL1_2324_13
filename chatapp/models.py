from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
    friends = models.ManyToManyField(User, related_name='friendRoom')

    def __str__(self):
        friends_usernames = [user.username for user in self.friends.all()]
        return f"Chat between {', '.join(friends_usernames)}"

class Messages(models.Model):
    chatRoom = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyer')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_reçus')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"