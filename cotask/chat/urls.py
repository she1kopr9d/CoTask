import django.urls

import chat.views


app_name = "chat"

urlpatterns = [
    django.urls.path("<str:chat_id>/", chat.views.chat_room, name="chat_room"),
    django.urls.path("", chat.views.chat_list_view, name="chat_list"),
    django.urls.path(
        "chat_with/<str:username>/",
        chat.views.chat_with_user,
        name="chat_with_user",
    ),
]
