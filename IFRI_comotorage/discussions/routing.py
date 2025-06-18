from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<discussion_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]


# Exemple 1: Si votre modèle utilise un UUID au lieu d'un simple \w+
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<discussion_id>[0-9a-f-]+)/$', consumers.ChatConsumer.as_asgi()),
]

# Exemple 2: Si vous avez un modèle Room/Channel avec slug
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_slug>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
]

# Exemple 3: Si vous avez besoin d'authentification utilisateur
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<discussion_id>\w+)/(?P<user_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]

# Exemple 4: Si votre modèle utilise des IDs numériques
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<discussion_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]

# Exemple 5: Plusieurs types de chat (privé, groupe, public)
websocket_urlpatterns = [
    re_path(r'ws/chat/private/(?P<discussion_id>\w+)/$', consumers.PrivateChatConsumer.as_asgi()),
    re_path(r'ws/chat/group/(?P<group_id>\w+)/$', consumers.GroupChatConsumer.as_asgi()),
    re_path(r'ws/chat/public/(?P<room_name>\w+)/$', consumers.PublicChatConsumer.as_asgi()),
]

# Exemple 6: Chat avec support de sous-canaux
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<discussion_id>\w+)/(?P<channel_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

# Exemple 7: Si vous utilisez des paths plus complexes
websocket_urlpatterns = [
    re_path(r'ws/discussions/(?P<discussion_id>\w+)/messages/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/notifications/(?P<user_id>\d+)/$', consumers.NotificationConsumer.as_asgi()),
]