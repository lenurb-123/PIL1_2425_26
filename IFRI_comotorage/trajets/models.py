from django.db import models
from django.utils import timezone
from comptes.models import Utilisateur
from django import forms


# Jours de la semaine pour les trajets récurrents
JOURS_CHOICES = [
    ('Lun', 'Lundi'),
    ('Mar', 'Mardi'),
    ('Mer', 'Mercredi'),
    ('Jeu', 'Jeudi'),
    ('Ven', 'Vendredi'),
    ('Sam', 'Samedi'),
    ('Dim', 'Dimanche'),
]

STATUT_CHOICES = [
    ('proposé', 'Proposé'),
    ('accepté', 'Accepté'),
    ('terminé', 'Terminé'),
    ('annulé', 'Annulé'),
]

class Trajet(models.Model):
    conducteur_nom = models.CharField(max_length=100, default="")
    conducteur_prenom = models.CharField(max_length=100, default="")
    depart = models.CharField(max_length=255, default="")
    arrivee = models.CharField(max_length=255, default="")
    heure_depart = models.DateTimeField(default=timezone.now)
    heure_arrivee = models.DateTimeField(default=timezone.now)
    places_disponibles = models.PositiveIntegerField(default=1)
    tarif = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.depart} -> {self.arrivee} par {self.conducteur_nom}"

class Reservation(models.Model):
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, related_name='reservations')
    passager_nom = models.CharField(max_length=100, default="")
    passager_prenom = models.CharField(max_length=100, default="")
    depart = models.CharField(max_length=255, default="")
    arrivee = models.CharField(max_length=255, default="")
    heure_depart = models.DateTimeField(default=timezone.now)
    heure_arrivee = models.DateTimeField(default=timezone.now)
    places_reservees = models.PositiveIntegerField(default=1)
    date_reservation = models.DateTimeField(auto_now_add=True)
    created_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Réservation de {self.passager_nom} pour {self.trajet}"

class Avis(models.Model):
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, related_name='avis')
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='avis_donnes')
    destinataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='avis_recus')
    note = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    commentaire = models.TextField(blank=True)
    
    def __str__(self):
        return f"Avis de {self.auteur.username} pour {self.destinataire.username}"

class TrajetTaxi(models.Model):
    conducteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    lieu_depart = models.CharField(max_length=255, default="")
    lieu_arrivee = models.CharField(max_length=255, default="")
    heure_depart = models.TimeField(null=True, blank=True)  # Permet les valeurs nulles
    jours_semaine = models.CharField(max_length=50, default="")
    places_disponibles = models.PositiveIntegerField(default=1)
    date_creation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='proposé')
    tarif = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.conducteur} - {self.lieu_depart} → {self.lieu_arrivee}"

class TrajetPassage(models.Model):
    passager = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    lieu_depart = models.CharField(max_length=255)
    lieu_arrivee = models.CharField(max_length=255, default="IFRI UAC Bénin")
    heure_souhaitee = models.TimeField(null=True, blank=True)  # Permet les valeurs nulles
    jours_semaine = models.CharField(max_length=50)
    date_creation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='proposé')
    tarif = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.passager} - {self.lieu_depart} → {self.lieu_arrivee}"

class PositionUtilisateur(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.utilisateur} ({self.latitude}, {self.longitude})"