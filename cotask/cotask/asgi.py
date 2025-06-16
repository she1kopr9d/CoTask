import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cotask.settings")
django.setup()

import channels.routing
import channels.auth
import cotask.routing


application = channels.routing.ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": channels.auth.AuthMiddlewareStack(
            channels.routing.URLRouter(cotask.routing.websocket_urlpatterns)
        ),
    }
)
