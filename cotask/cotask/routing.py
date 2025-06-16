import django.urls

import chat.consumers


websocket_urlpatterns = [
    django.urls.path(
        "ws/chat/<str:chat_id>/",
        chat.consumers.ChatConsumer.as_asgi(),
    ),
]
