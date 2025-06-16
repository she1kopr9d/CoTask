import django.contrib.auth.models
import django.contrib.auth.decorators
import django.db.models
import django.shortcuts

import chat.models


@django.contrib.auth.decorators.login_required
def chat_room(request, chat_id):
    chat_obj = django.shortcuts.get_object_or_404(chat.models.Chat, pk=chat_id)
    messages = chat_obj.messages.select_related("sender").order_by("timestamp")

    return django.shortcuts.render(
        request,
        "chat/chat_room.html",
        {
            "room_name": chat_id,
            "messages": messages,
            "username": request.user.username,
        },
    )


@django.contrib.auth.decorators.login_required
def chat_list_view(request):
    chats = chat.models.Chat.objects.filter(participants=request.user)
    return django.shortcuts.render(
        request, "chat/chat_list.html", {"chats": chats}
    )


@django.contrib.auth.decorators.login_required
def chat_with_user(request, username):
    other_user = django.shortcuts.get_object_or_404(
        django.contrib.auth.models.User, username=username
    )
    if other_user == request.user:
        return django.shortcuts.redirect("chat:chat_list")
    chats = (
        chat.models.Chat.objects.filter(participants=request.user)
        .filter(participants=other_user)
        .distinct()
    )
    chats = chats.annotate(
        num_members=django.db.models.Count("participants")
    ).filter(num_members=2)

    if chats.exists():
        chat_obj = chats.first()
    else:
        chat_obj = chat.models.Chat.objects.create()
        chat_obj.participants.add(request.user, other_user)
        chat_obj.save()
    return django.shortcuts.redirect("chat:chat_room", chat_obj.id)
