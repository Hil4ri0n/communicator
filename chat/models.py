from django.core.exceptions import ValidationError
from django.db import models
from users_and_profiles.models import Profile


class ChatRoom(models.Model):
    participants = models.ManyToManyField(Profile)

    def __str__(self):
        participant_names = [participant.nickname for participant in self.participants.all()]
        names_str = ", ".join(participant_names)
        return f"Chatroom of {names_str}"

    def get_last_viewed_message(self, sender_id):
        return Message.objects.filter(
            chat_room=self,
            sender_id=sender_id,
            viewed=True
        ).order_by('-timestamp').first()

    def count_unread_messages(self, sender_id):
        return Message.objects.filter(
            chat_room=self,
            sender_id=sender_id,
            viewed=False).count()


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} on {self.timestamp}"

    def __str__(self):
        name = "ChatRoom of"
        for participant in self.participants:
            name += f" and {participant.nickname}"
        return name
