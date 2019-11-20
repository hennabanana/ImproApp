from django.urls import path

from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from backend.api.consumers import ImproConsumer
from backend.api.token_auth import TokenAuthMiddlewareStack

#Router des Websockets/Channel
application = ProtocolTypeRouter({
    "websocket": TokenAuthMiddlewareStack(
        URLRouter([
            path("ws/", ImproConsumer),
            #userid wurde als variable mitgegeben
            path("ws/<userid>", ImproConsumer),
        ]),
    ),
})