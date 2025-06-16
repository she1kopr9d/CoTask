import django.contrib.admin

import chat.models


django.contrib.admin.site.register(
    chat.models.Chat,
)
django.contrib.admin.site.register(
    chat.models.Message,
)
