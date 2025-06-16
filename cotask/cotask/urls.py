import cotask.settings

import django.contrib
import django.contrib.admin
import django.urls
import django.conf.urls.i18n
import django.conf.urls.static


urlpatterns = [
    django.urls.path("admin/", django.contrib.admin.site.urls),
]


urlpatterns += [
    django.urls.path("i18n/", django.urls.include("django.conf.urls.i18n")),
]

urlpatterns += django.conf.urls.i18n.i18n_patterns(
    django.urls.path("", django.urls.include("guest.urls")),
    django.urls.path("user/", django.urls.include("user.urls")),
    django.urls.path("", django.urls.include("social_media.urls")),
    django.urls.path("cards/", django.urls.include("remember_line.urls")),
    django.urls.path(
        "chat/", django.urls.include("chat.urls", namespace="chat")
    ),
    prefix_default_language=True,
)

if cotask.settings.DEBUG:
    urlpatterns += django.conf.urls.static.static(
        cotask.settings.MEDIA_URL,
        document_root=cotask.settings.MEDIA_ROOT,
    )
