import django.contrib.auth.models
import django.db.models


class Chat(django.db.models.Model):
    class ChatType(django.db.models.TextChoices):
        PRIVATE = 'private', 'Личный'
        GROUP = 'group', 'Групповой'

    chat_type = django.db.models.CharField(
        max_length=10,
        choices=ChatType.choices,
        default=ChatType.PRIVATE,
    )
    participants = django.db.models.ManyToManyField(
        django.contrib.auth.models.User, related_name="chats"
    )
    created_at = django.db.models.DateTimeField(auto_now_add=True)

    def is_private(self):
        return self.chat_type == self.ChatType.PRIVATE

    def is_group(self):
        return self.chat_type == self.ChatType.GROUP


class Message(django.db.models.Model):
    chat = django.db.models.ForeignKey(
        Chat, on_delete=django.db.models.CASCADE, related_name="messages"
    )
    sender = django.db.models.ForeignKey(
        django.contrib.auth.models.User, on_delete=django.db.models.CASCADE
    )
    text = django.db.models.TextField()
    timestamp = django.db.models.DateTimeField(auto_now_add=True)
