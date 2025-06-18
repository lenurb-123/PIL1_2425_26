from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
import json
from django.utils import timezone

def send_notification(user, type_notif, titre, message, lien=None):
    """
    Envoie une notification à un utilisateur spécifique.
    La notification est sauvegardée en base de données et envoyée en temps réel via WebSocket.
    """
    # Créer la notification dans la base de données
    notification = Notification.objects.create(
        user=user,
        type=type_notif,
        titre=titre,
        message=message,
        lien=lien
    )

    # Préparer les données de la notification
    notification_data = {
        'id': notification.id,
        'type': notification.type,
        'titre': notification.titre,
        'message': notification.message,
        'lien': notification.lien,
        'date_creation': timezone.localtime(notification.date_creation).strftime('%Y-%m-%d %H:%M:%S')
    }

    # Envoyer la notification via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'user_notifications_{user.id}',
        {
            'type': 'notification',
            'notification': notification_data
        }
    )

    return notification 