from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import pyotp

# --- Choix possibles pour le rôle de l'utilisateur ---
ROLE_CHOICES = (
    ('conducteur', 'Conducteur'),
    ('passager', 'Passager'),
)



# --- Manager personnalisé pour créer les utilisateurs et super-utilisateurs ---
class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse e-mail est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hash du mot de passe
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# --- Modèle utilisateur personnalisé ---
class Utilisateur(AbstractBaseUser, PermissionsMixin):
    # Identifiants et infos de contact
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True, null=True)

    # Infos véhicule (pour conducteurs)
    vehicule = models.CharField(max_length=100, blank=True, null=True)
    immatriculation = models.CharField(max_length=20, blank=True, null=True)

    # Données personnelles
    date_naissance = models.DateField(null=True, blank=True)
    adresse = models.CharField(max_length=200, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    departement = models.CharField(max_length=100, blank=True, null=True)

    # Photo de profil
    photo_profil = models.ImageField(upload_to='profils/', blank=True, null=True)

    # Dates et statut
    date_inscription = models.DateTimeField(auto_now_add=True)
    derniere_connexion = models.DateTimeField(null=True, blank=True)
    est_verifie = models.BooleanField(default=False)
    est_actif = models.BooleanField(default=True)
    est_bloque = models.BooleanField(default=False)
    date_blocage = models.DateTimeField(null=True, blank=True)
    raison_blocage = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(default=timezone.now, null=True, blank=True)

    # Rôle utilisateur : conducteur ou passager
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='passager')

    # Informations profil utilisateur
    adresse_depart_habituelle = models.CharField(max_length=100, blank=True)
    heure_depart_habituelle = models.TimeField(blank=True, null=True)
    heure_arrivee_habituelle = models.TimeField(blank=True, null=True)
    # Infos véhicule (conducteur)
    marque_vehicule = models.CharField(max_length=100, blank=True)
    modele_vehicule = models.CharField(max_length=100, blank=True)
    places_disponibles = models.PositiveIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(1)]
    )

    # Statuts pour Django auth
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Double authentification (2FA)
    deux_facteurs_active = models.BooleanField(default=False, verbose_name="2FA activée")
    deux_facteurs_code = models.CharField(max_length=6, blank=True, null=True, verbose_name="Code 2FA")
    deux_facteurs_code_expiration = models.DateTimeField(blank=True, null=True, verbose_name="Expiration code 2FA")

    # Champs pour 2FA
    two_factor_enabled = models.BooleanField(default=False)
    totp_secret = models.CharField(max_length=32, blank=True, null=True)

    # Champs requis pour Django authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    objects = UtilisateurManager()

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.role} - {self.telephone})"

    def get_initials(self):
        if self.prenom and self.nom:
            return f"{self.prenom[0]}{self.nom[0]}".upper()
        return self.nom[0].upper()

    def get_full_name(self):
        if self.prenom and self.nom:
            return f"{self.prenom} {self.nom}"
        return self.nom

    # Validation personnalisée : immatriculation obligatoire si conducteur
    def clean(self):
        if self.role == 'conducteur' and not self.immatriculation:
            raise ValidationError({'immatriculation': "L'immatriculation est obligatoire pour les conducteurs."})

    def enable_2fa(self):
        """Active l'authentification à deux facteurs pour l'utilisateur"""
        if not self.totp_secret:
            self.totp_secret = pyotp.random_base32()
        self.two_factor_enabled = True
        self.save()
        
    def disable_2fa(self):
        """Désactive l'authentification à deux facteurs pour l'utilisateur"""
        self.two_factor_enabled = False
        self.totp_secret = None
        self.save()
        
    def get_totp_uri(self):
        """Génère l'URI pour le QR code TOTP"""
        if self.totp_secret:
            totp = pyotp.TOTP(self.totp_secret)
            return totp.provisioning_uri(
                name=self.email,
                issuer_name="IFRI Comotorage"
            )
        return None
        
    def verify_totp(self, token):
        """Vérifie un token TOTP"""
        if self.totp_secret and token:
            totp = pyotp.TOTP(self.totp_secret)
            return totp.verify(token)
        return False

    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')
        db_table = 'comptes_utilisateur'


# --- Modèle pour stocker les messages entre utilisateurs dans une discussion ---
class Message(models.Model):
    discussion = models.ForeignKey('discussions.Discussion', related_name='comptes_messages', on_delete=models.CASCADE)
    expediteur = models.ForeignKey(Utilisateur, related_name='comptes_messages_envoyes', on_delete=models.CASCADE)
    destinataire = models.ForeignKey(Utilisateur, related_name='comptes_messages_recus', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoie = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    # Possibilité de joindre un fichier au message
    fichier = models.FileField(upload_to='messages_fichiers/', blank=True, null=True)

    class Meta:
        ordering = ['date_envoie']

    def __str__(self):
        return f"{self.expediteur} → {self.destinataire} : {self.contenu[:30]}"


# --- Modèle pour gérer les notifications envoyées aux utilisateurs ---
class Notification(models.Model):
    TYPE_CHOICES = (
        ('message', 'Nouveau message'),
        ('trajet', 'Nouveau trajet'),
        ('matching', 'Matching trouvé'),
        ('system', 'Notification système'),
    )

    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    titre = models.CharField(max_length=100)
    message = models.TextField()
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    lien = models.CharField(max_length=200, blank=True, null=True)  # URL ou route liée à la notification

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} - {self.user.email}"


# --- Abonnement à une newsletter ---
class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.email



# --- Conversation entre plusieurs utilisateurs (privée ou groupe) ---
class Conversation(models.Model):
    TYPE_CHOICES = [
        ('private', 'Privé'),
        ('group', 'Groupe'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='private')
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Participants via modèle intermédiaire Participant
    participants = models.ManyToManyField(Utilisateur, through='Participant', related_name='user_conversations')

    def __str__(self):
        return self.name if self.name else f"Conversation {self.id}"


# --- Lien entre un utilisateur et une conversation ---
class Participant(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='conversation_participants')
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='user_participations')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ('conversation', 'user')


# --- Messages dans une conversation (chat) ---
class ChatMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message de {self.sender.get_full_name()} dans {self.conversation}"


# --- Réservation d'une place sur un trajet par un passager ---
# (Modèle supprimé, utiliser celui de trajets)
