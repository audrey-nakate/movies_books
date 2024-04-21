"""
ASGI config for movies_books project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
# modifications made to the asgi file since we are using django channels for websockets and message sending and receiving
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import movies_books_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies_books.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            movies_books_app.routing.websocket_urlpatterns
        )
    ),
})