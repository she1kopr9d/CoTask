import django.http
import django.shortcuts


def index(request: django.http.HttpRequest):
    if request.user.is_authenticated:
        return django.shortcuts.redirect("feed")
    return django.shortcuts.render(request, "guest/main.html")
