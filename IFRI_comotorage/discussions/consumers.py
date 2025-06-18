import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Discussion, Message
from django.contrib.auth import get_user_model
from comptes.utils import send_notification
from asgiref.sync import sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.discussion_id = self.scope['url_route']['kwargs']['discussion_id']
        self.room_group_name = f'chat_{self.discussion_id}'
        self.user = self.scope["user"]

        # Vérifier si l'utilisateur a accès à cette discussion
        if not await self.can_access_discussion():
            await self.close()
            return

        # Rejoindre le groupe de discussion
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe de discussion
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Sauvegarder le message et obtenir les destinataires
        message_data = await self.save_message(message)
        
        # Envoyer le message au groupe
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.user.id,
                'sender_name': f"{self.user.prenom} {self.user.nom}",
                'timestamp': message_data['timestamp']
            }
        )

        # Envoyer des notifications aux utilisateurs qui ne sont pas actuellement dans la discussion
        await self.send_message_notifications(message_data)

    async def chat_message(self, event):
        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def can_access_discussion(self):
        try:
            discussion = Discussion.objects.get(id=self.discussion_id)
            return discussion.participants.filter(id=self.user.id).exists()
        except Discussion.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, content):
        discussion = Discussion.objects.get(id=self.discussion_id)
        message = Message.objects.create(
            discussion=discussion,
            expediteur=self.user,
            contenu=content
        )
        return {
            'timestamp': message.date_envoie.isoformat(),
            'discussion_name': discussion.nom or f"Discussion avec {self.user.get_full_name()}",
            'recipients': list(discussion.participants.exclude(id=self.user.id))
        }

    @sync_to_async
    def send_message_notifications(self, message_data):
        for recipient in message_data['recipients']:
            send_notification(
                user=recipient,
                type_notif='message',
                titre=f'Nouveau message de {self.user.get_full_name()}',
                message=f'Dans {message_data["discussion_name"]}',
                lien=f'/discussions/{self.discussion_id}/'
            )
