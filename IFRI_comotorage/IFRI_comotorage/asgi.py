import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IFRI_comotorage.settings')
django.setup()  # ✅ obligatoire avant d'importer discussions.routing

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import discussions.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            discussions.routing.websocket_urlpatterns
        )
    ),
})

import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IFRI_comotorage.settings')
django.setup()
application = get_default_application()
