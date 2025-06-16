import django.contrib.auth.models
import django.db.models


class Chat(django.db.models.Model):
    participants = django.db.models.ManyToManyField(
        django.contrib.auth.models.User, related_name="chats"
    )
    created_at = django.db.models.DateTimeField(auto_now_add=True)


class Message(django.db.models.Model):
    chat = django.db.models.ForeignKey(
        Chat, on_delete=django.db.models.CASCADE, related_name="messages"
    )
    sender = django.db.models.ForeignKey(
        django.contrib.auth.models.User, on_delete=django.db.models.CASCADE
    )
    text = django.db.models.TextField()
    timestamp = django.db.models.DateTimeField(auto_now_add=True)
