from django.db import models
from comptes.models import Utilisateur, Notification
from django.conf import settings
from django.utils import timezone

class Discussion(models.Model):
    TYPE_CHOICES = [
        ('privee', 'Privée'),
        ('groupe', 'Groupe'),
    ]
    CONFIDENTIALITE_CHOICES = [
        ('public', 'Public'),
        ('prive', 'Privé'),
        ('secret', 'Secret'),
    ]
    
    nom = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='privee')
    confidentialite = models.CharField(max_length=10, choices=CONFIDENTIALITE_CHOICES, default='public')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='discussions')
    # Ajout d'un créateur pour les discussions de groupe
    createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='discussions_creees', null=True, blank=True)
    photo = models.ImageField(upload_to='discussions/photos/', null=True, blank=True)
    description = models.TextField(blank=True)  # Ajout d'une description
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    statut = models.CharField(max_length=20, choices=[('active', 'Active'), ('archivee', 'Archivée')], default='active')

    class Meta:
        ordering = ['-date_modification']

    def __str__(self):
        if self.type == 'privee' and self.participants.count() >= 2:
            participants_list = list(self.participants.all())
            if len(participants_list) >= 2:
                return f"Chat privé: {participants_list[0].prenom} {participants_list[0].nom} - {participants_list[1].prenom} {participants_list[1].nom}"
        return self.nom or f"Discussion {self.id}"

    def dernier_message(self):
        return self.messages.order_by('-date_envoi').first()

    def nombre_messages_non_lus(self, utilisateur):
        """Retourne le nombre de messages non lus pour un utilisateur donné"""
        return self.messages.filter(lu=False, destinataire=utilisateur).count()

    def marquer_messages_comme_lus(self, utilisateur):
        """Marque tous les messages comme lus pour un utilisateur"""
        self.messages.filter(destinataire=utilisateur, lu=False).update(lu=True)

class Message(models.Model):
    TYPE_CHOICES = [
        ('text', 'Texte'),
        ('media', 'Média'),
        ('system', 'Système'),  # Pour les messages système (join, leave, etc.)
    ]

    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Vidéo'),
        ('audio', 'Audio'),  # Pour les messages vocaux
        ('document', 'Document'),
    ]
    
    # Relations - UN SEUL champ discussion
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='messages')
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='messages_envoyes')
    # Pour les discussions de groupe, destinataire peut être null
    destinataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='messages_recus', null=True, blank=True)
    
    # Contenu - UN SEUL champ contenu
    contenu = models.TextField(blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='text')
    
    # Média
    media = models.FileField(upload_to='messages/media/', null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, null=True, blank=True)
    
    # Dates
    date_envoi = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)  # Pour les messages modifiés
    
    # États
    lu = models.BooleanField(default=False)
    supprime = models.BooleanField(default=False)  # Soft delete
    
    # Réponses
    message_parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='reponses')

    class Meta:
        ordering = ['date_envoi']

    def __str__(self):
        if self.discussion.type == 'groupe':
            return f"Message de {self.expediteur.nom} dans {self.discussion.nom}"
        return f"Message de {self.expediteur.nom} à {self.destinataire.nom if self.destinataire else 'Groupe'}"

    def save(self, *args, **kwargs):
        # Auto-détection du type de média
        if self.media:
            self.type = 'media'
            extension = self.media.name.lower().split('.')[-1]
            
            if extension in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
                self.media_type = 'image'
            elif extension in ['mp4', 'avi', 'mov', 'webm', 'mkv']:
                self.media_type = 'video'
            elif extension in ['mp3', 'wav', 'ogg', 'm4a']:
                self.media_type = 'audio'
            else:
                self.media_type = 'document'
        
        super().save(*args, **kwargs)
        
        # Mettre à jour la date de modification de la discussion
        from django.utils import timezone
        self.discussion.date_modification = timezone.now()
        self.discussion.save(update_fields=['date_modification'])
# Modèle pour gérer les statuts de lecture dans les discussions de groupe
class StatutLectureMessage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='statuts_lecture')
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    lu = models.BooleanField(default=False)
    date_lecture = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['message', 'utilisateur']

    def save(self, *args, **kwargs):
        if self.lu and not self.date_lecture:
            self.date_lecture = timezone.now()
        super().save(*args, **kwargs)


class Appel(models.Model):
    emetteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='appels_emis')
    recepteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='appels_recus')
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=[('audio', 'Audio'), ('video', 'Vidéo')])

# Modèle pour les paramètres de discussion par utilisateur
class ParametresDiscussion(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    notifications = models.BooleanField(default=True)
    epingle = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)
    couleur = models.CharField(max_length=7, null=True, blank=True)  # Code couleur hex
    
    class Meta:
        unique_together = ['utilisateur', 'discussion']

# Modèle pour l'historique des actions (optionnel)
class ActionDiscussion(models.Model):
    TYPE_ACTION_CHOICES = [
        ('creation', 'Création'),
        ('ajout_participant', 'Ajout participant'),
        ('suppression_participant', 'Suppression participant'),
        ('changement_nom', 'Changement de nom'),
        ('changement_photo', 'Changement de photo'),
    ]
    
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='actions')
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    type_action = models.CharField(max_length=30, choices=TYPE_ACTION_CHOICES)
    details = models.JSONField(null=True, blank=True)  # Détails supplémentaires
    date_action = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_action']

# Suppression du modèle Conversation car redondant avec Discussion