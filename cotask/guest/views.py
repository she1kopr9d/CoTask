import django.shortcuts


def index(request):
    return django.shortcuts.render(request, "guest/main.html")
