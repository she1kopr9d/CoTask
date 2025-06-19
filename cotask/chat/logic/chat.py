import chat.models


def get_all_private_chats(user) -> list:
    chats = chat.models.Chat.objects.filter(
        participants=user,
        chat_type=chat.models.Chat.ChatType.PRIVATE,
    )
    chat_data = []
    for chat_obj in chats:
        if chat_obj.is_private():
            partner = chat_obj.participants.exclude(id=user.id).first()
            chat_data.append({
                "chat": chat_obj,
                "partner": partner,
                "unread_count": 0,#chat_obj.get_unread_count_for_user(request.user),
            })
    return chat_data
