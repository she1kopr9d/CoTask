import django.contrib.auth.models
import django.contrib.auth.decorators
import django.db.models
import django.shortcuts

import chat.models
import chat.logic.chat


@django.contrib.auth.decorators.login_required
def chat_room(request, chat_id):
    chat_obj = django.shortcuts.get_object_or_404(chat.models.Chat, pk=chat_id)
    messages = chat_obj.messages.select_related("sender").order_by("timestamp")
    partner = chat_obj.participants.exclude(username=request.user.username).first()

    return django.shortcuts.render(
        request,
        "chat/chat_room.html",
        {
            "room_name": chat_id,
            "messages": messages,
            "username": request.user.username,
            "partner": partner,
            "chat_list": chat.logic.chat.get_all_private_chats(request.user),
        },
    )


@django.contrib.auth.decorators.login_required
def chat_list_view(request):
    return django.shortcuts.render(
        request,
        "chat/chat_list.html",
        {
            "chats": chat.logic.chat.get_all_private_chats(request.user),
        },
    )


@django.contrib.auth.decorators.login_required
def chat_with_user(request, username):
    other_user = django.shortcuts.get_object_or_404(
        django.contrib.auth.models.User, username=username
    )
    if other_user == request.user:
        return django.shortcuts.redirect("chat:chat_list")
    chats = (
        chat.models.Chat.objects.filter(
            participants=request.user,
            chat_type=chat.models.Chat.ChatType.PRIVATE,
        ).filter(participants=other_user)
    )
    chat_obj = chats.first()
    if chat_obj is None:
        chat_obj = chat.models.Chat.objects.create()
        chat_obj.participants.add(request.user, other_user)
        chat_obj.save()
    return django.shortcuts.redirect("chat:chat_room", chat_obj.id)
