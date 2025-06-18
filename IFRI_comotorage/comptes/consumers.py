import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        if not self.user.is_authenticated:
            await self.close()
            return

        # Créer un groupe unique pour l'utilisateur
        self.notification_group_name = f'user_notifications_{self.user.id}'
        
        # Rejoindre le groupe
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Envoyer les notifications non lues au moment de la connexion
        await self.send_unread_notifications()

    async def disconnect(self, close_code):
        # Quitter le groupe
        if hasattr(self, 'notification_group_name'):
            await self.channel_layer.group_discard(
                self.notification_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('action') == 'mark_as_read':
            notification_id = data.get('notification_id')
            await self.mark_notification_as_read(notification_id)

    async def notification(self, event):
        # Envoyer la notification au WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': event['notification']
        }))

    @database_sync_to_async
    def mark_notification_as_read(self, notification_id):
        try:
            notification = Notification.objects.get(
                id=notification_id,
                user=self.user
            )
            notification.lu = True
            notification.save()
        except Notification.DoesNotExist:
            pass

    @database_sync_to_async
    def get_unread_notifications(self):
        return list(Notification.objects.filter(
            user=self.user,
            lu=False
        ).values('id', 'type', 'titre', 'message', 'date_creation'))

    async def send_unread_notifications(self):
        notifications = await self.get_unread_notifications()
        if notifications:
            await self.send(text_data=json.dumps({
                'type': 'unread_notifications',
                'notifications': notifications
            })) 