from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import backend.routing


application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            backend.routing.websocket_urlpatterns
        )
    )
})
