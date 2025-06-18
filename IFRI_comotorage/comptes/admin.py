from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Utilisateur, Message, Notification, Newsletter, Conversation, Participant, ChatMessage
from trajets.models import TrajetTaxi, TrajetPassage

# Admin pour l'utilisateur personnalisé
@admin.register(Utilisateur)
class UtilisateurAdmin(BaseUserAdmin):
    list_display = ('email', 'prenom', 'nom', 'role', 'is_active', 'est_verifie', 'date_inscription')
    list_filter = ('role', 'is_active', 'est_verifie', 'est_bloque')
    search_fields = ('email', 'prenom', 'nom', 'telephone')
    ordering = ('-date_inscription',)
    readonly_fields = ('date_inscription', 'derniere_connexion', 'date_derniere_modification', 'date_blocage')

    fieldsets = (
        (_('Informations personnelles'), {
            'fields': ('email', 'nom', 'prenom', 'telephone', 'photo_profil', 'photo', 'date_naissance', 'adresse', 'ville', 'departement')
        }),
        (_('Rôle & véhicule'), {
            'fields': ('role', 'vehicule', 'immatriculation', 'marque_vehicule', 'modele_vehicule', 'places_disponibles')
        }),
        (_('Habitudes de trajet'), {
            'fields': ('adresse_depart', 'heure_depart_habituelle', 'heure_arrivee_habituelle')
        }),
        (_('Statut & sécurité'), {
            'fields': ('is_active', 'is_staff', 'est_verifie', 'est_bloque', 'raison_blocage', 'date_blocage', 'deux_facteurs_active', 'deux_facteurs_code', 'deux_facteurs_code_expiration')
        }),
        (_('Dates'), {
            'fields': ('date_inscription', 'derniere_connexion', 'date_derniere_modification')
        }),
        (_('Permissions'), {
            'fields': ('is_superuser', 'groups', 'user_permissions'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'prenom', 'password1', 'password2', 'role', 'is_staff', 'is_superuser'),
        }),
    )

# Admin pour les messages directs
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('expediteur', 'destinataire', 'date_envoie', 'lu')
    list_filter = ('lu',)
    search_fields = ('expediteur__email', 'destinataire__email', 'contenu')

# Admin pour les notifications
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'titre', 'lu', 'date_creation')
    list_filter = ('type', 'lu')
    search_fields = ('user__email', 'titre', 'message')

# Admin pour les newsletters
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_inscription', 'actif')
    search_fields = ('email',)

# Admin pour les conversations
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'name', 'created_at', 'updated_at')
    list_filter = ('type',)
    search_fields = ('name',)

# Admin pour les participants
@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'conversation', 'joined_at', 'is_admin')
    list_filter = ('is_admin',)

# Admin pour les messages de chat
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'created_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('sender__email', 'content')

# Admin pour les trajets
@admin.register(TrajetTaxi)
class TrajetConducteurAdmin(admin.ModelAdmin):
    list_display = ('conducteur', 'lieu_depart', 'lieu_arrivee', 'heure_depart', 'places_disponibles', 'statut')
    list_filter = ('statut', 'jours_semaine')
    search_fields = ('lieu_depart', 'lieu_arrivee', 'conducteur__email')

@admin.register(TrajetPassage)
class TrajetPassagerAdmin(admin.ModelAdmin):
    list_display = ('passager', 'lieu_depart', 'lieu_arrivee', 'heure_souhaitee', 'statut')
    list_filter = ('statut', 'jours_semaine')
    search_fields = ('lieu_depart', 'lieu_arrivee', 'passager__email')
