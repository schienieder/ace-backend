"""
ASGI config for ace project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from api.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ace.settings")

application = ProtocolTypeRouter(
    {"http": get_asgi_application(), "websocket": URLRouter(websocket_urlpatterns)}
)
