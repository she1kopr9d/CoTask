import cotask.settings

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
]


urlpatterns += [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("", include("guest.urls")),
    path("user/", include("user.urls")),
    path("", include("social_media.urls")),
    prefix_default_language=True,  # URL без префикса для языка по умолчанию
)

if cotask.settings.DEBUG:
    urlpatterns += static(cotask.settings.MEDIA_URL, document_root=cotask.settings.MEDIA_ROOT)
