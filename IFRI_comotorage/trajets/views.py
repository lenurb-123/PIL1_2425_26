from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TrajetConducteurForm, TrajetPassagerForm, RechercheTrajetForm
from .models import TrajetTaxi, TrajetPassage, Trajet, Reservation
from datetime import datetime, timedelta
from django.urls import reverse
from django.db.models import Q
from trajets.models import TrajetTaxi, TrajetPassage
import math
from .utils import (
    notifier_nouveau_trajet, 
    notifier_reservation, 
    notifier_statut_reservation, 
    notifier_rappel_trajet,
    notifier_annulation_trajet,
    calculer_score_matching
)
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from urllib.parse import unquote
import re
import logging

logger = logging.getLogger(__name__)

@login_required
def recherche_trajet(request):
    
    return render(request, 'trajets/recherche_trajet.html')

# Publication de trajet - conducteur
@login_required
def publier_trajet_conducteur(request):
    if request.method == 'POST':
        form = TrajetConducteurForm(request.POST)
        if form.is_valid():
            trajet = form.save(commit=False)
            trajet.conducteur = request.user
            trajet.save()
            
            # Envoyer des notifications aux passagers potentiellement intéressés
            notifier_nouveau_trajet(trajet, 'conducteur')
            
            return redirect('mes_trajets')
    else:
        form = TrajetConducteurForm()
    return render(request, 'trajets/publier_conducteur.html', {'form': form})


# Publication de trajet - passager
@login_required
def publier_trajet_passager(request):
    if request.method == 'POST':
        form = TrajetPassagerForm(request.POST)
        if form.is_valid():
            trajet = form.save(commit=False)
            trajet.passager = request.user
            trajet.save()
            
            # Envoyer des notifications aux conducteurs potentiellement intéressés
            notifier_nouveau_trajet(trajet, 'passager')
            
            return redirect('mes_trajets')
    else:
        form = TrajetPassagerForm()
    return render(request, 'trajets/publier_passager.html', {'form': form})


# Vue de matching passager → conducteur (moderne, authentique)
def matching_view(request, passager_id):
    passager_trajet = get_object_or_404(TrajetPassage, id=passager_id)
    candidats = TrajetTaxi.objects.all()
    correspondances = []
    for trajet in candidats:
        # 1. Places disponibles
        if trajet.places_disponibles < 1:
            continue
        # 2. Calcul du score global (moderne)
        score = calculer_score_matching(trajet, passager_trajet)
        if score > 0:
            correspondances.append((trajet, score))
    correspondances.sort(key=lambda x: x[1], reverse=True)
    return render(request, 'trajets/resultats_matching.html', {
        'passager_trajet': passager_trajet,
        'resultats': correspondances,
    })


# Affichage global des trajets sur carte avec filtres (adresses uniquement)
def carte_trajets(request):
    role = request.GET.get('role')
    jour = request.GET.get('jour')
    trajets_conducteurs = TrajetTaxi.objects.all()
    trajets_passagers = TrajetPassage.objects.all()
    if jour:
        trajets_conducteurs = trajets_conducteurs.filter(jours_semaine__icontains=jour)
        trajets_passagers = trajets_passagers.filter(jours_semaine__icontains=jour)
    if role == 'conducteur':
        trajets_passagers = []  # n'afficher que les conducteurs
    elif role == 'passager':
        trajets_conducteurs = []  # n'afficher que les passagers
    return render(request, 'trajets/carte_trajets.html', {
        'trajets_conducteurs': trajets_conducteurs,
        'trajets_passagers': trajets_passagers,
        'role_selectionne': role,
        'jour_selectionne': jour,
    })

@login_required
def publier_trajet(request):
    # Affiche une page de choix moderne conducteur/passager
    return render(request, 'trajets/choix_publication.html')

@login_required
def rechercher_trajet(request):
    form = RechercheTrajetForm(request.GET or None)
    trajets_conducteurs = []
    scores = []

    if form.is_valid():
        depart = form.cleaned_data['depart'].strip()
        arrivee = form.cleaned_data['arrivee'].strip()

        # Créer un objet TrajetPassage temporaire pour le matching
        demande = TrajetPassage(
            lieu_depart=depart,
            lieu_arrivee=arrivee,
            heure_souhaitee=None,  # On ne demande pas l'heure dans la recherche simple
            jours_semaine="Lun,Mar,Mer,Jeu,Ven,Sam,Dim"  # On suppose tous les jours pour maximiser le matching
        )

        # Récupérer tous les trajets conducteurs disponibles
        tous_trajets = TrajetTaxi.objects.filter(places_disponibles__gt=0).select_related('conducteur')
        resultats = []
        for trajet in tous_trajets:
            score = calculer_score_matching(trajet, demande)
            if score > 0:
                resultats.append((trajet, score))
        # Trier par score décroissant
        resultats.sort(key=lambda x: x[1], reverse=True)
        trajets_conducteurs = [t[0] for t in resultats]
        scores = [t[1] for t in resultats]

    context = {
        'form': form,
        'trajets_conducteurs': trajets_conducteurs,
        'scores': scores,
    }
    return render(request, 'trajets/rechercher_trajet.html', context)

# Fonction pour calculer la distance approximative entre deux adresses
def calculer_distance_approximative(depart, arrivee):
    """
    Calcule une distance approximative basée sur les adresses
    Pour simplifier, on utilise une estimation basée sur la longueur des adresses
    """
    # Estimation basée sur la complexité des adresses
    longueur_depart = len(depart.strip())
    longueur_arrivee = len(arrivee.strip())
    
    # Distance de base (en km) - estimation
    distance_base = (longueur_depart + longueur_arrivee) / 10
    
    # Distance minimale de 1.2 km
    distance = max(1.2, distance_base)
    
    return round(distance, 1)

# Fonction pour calculer le tarif basé sur la distance
def calculer_tarif(distance_km):
    """
    Calcule le tarif basé sur la distance
    1.2 km = 200 FCFA
    """
    tarif_base = 200  # FCFA pour 1.2 km
    tarif_par_km = tarif_base / 1.2  # ~167 FCFA par km
    
    tarif = distance_km * tarif_par_km
    return round(tarif, 0)

def trajets_en_temps_reel(request):
    conducteurs = list(TrajetTaxi.objects.select_related('conducteur').all().values(
        'id', 'lieu_depart', 'lieu_arrivee', 'heure_depart', 'places_disponibles', 
        'date_creation', 'statut', 'tarif',
        'conducteur__prenom', 'conducteur__nom', 'conducteur__telephone', 'conducteur__photo_profil'
    ))
    passagers = list(TrajetPassage.objects.select_related('passager').all().values(
        'id', 'lieu_depart', 'lieu_arrivee', 'heure_souhaitee', 'date_creation', 
        'statut', 'tarif',
        'passager__prenom', 'passager__nom', 'passager__telephone', 'passager__photo_profil'
    ))
    
    # Formater les données des conducteurs
    for conducteur in conducteurs:
        distance = calculer_distance_approximative(conducteur['lieu_depart'], conducteur['lieu_arrivee'])
        conducteur['distance_km'] = distance
        conducteur['tarif_calcule'] = calculer_tarif(distance)
        conducteur['type'] = 'conducteur'
        # Ajouter les informations de l'utilisateur
        conducteur['utilisateur'] = {
            'prenom': conducteur.pop('conducteur__prenom'),
            'nom': conducteur.pop('conducteur__nom'),
            'telephone': conducteur.pop('conducteur__telephone'),
            'photo_profil': conducteur.pop('conducteur__photo_profil'),
        }
    
    # Formater les données des passagers
    for passager in passagers:
        passager['type'] = 'passager'
        # Ajouter les informations de l'utilisateur
        passager['utilisateur'] = {
            'prenom': passager.pop('passager__prenom'),
            'nom': passager.pop('passager__nom'),
            'telephone': passager.pop('passager__telephone'),
            'photo_profil': passager.pop('passager__photo_profil'),
        }
    
    return JsonResponse({
        'conducteurs': conducteurs,
        'passagers': passagers
    })

@login_required
def reserver_trajet(request, trajet_id):
    trajet = get_object_or_404(TrajetTaxi, id=trajet_id)
    
    # Vérifier si l'utilisateur n'a pas déjà réservé ce trajet
    if Reservation.objects.filter(trajet=trajet, passager=request.user).exists():
        messages.warning(request, "Vous avez déjà réservé ce trajet.")
        return redirect('details_trajet', trajet_id=trajet_id)
    
    # Vérifier s'il reste des places
    if trajet.places_disponibles < 1:
        messages.error(request, "Désolé, il n'y a plus de places disponibles pour ce trajet.")
        return redirect('rechercher_trajet')
    
    # Créer la réservation
    reservation = Reservation.objects.create(
        trajet=trajet,
        passager=request.user,
        statut='en_attente'
    )
    
    # Envoyer une notification au conducteur
    notifier_reservation(reservation)
    
    messages.success(request, "Votre demande de réservation a été envoyée au conducteur.")
    return redirect('mes_reservations')

@login_required
def gerer_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    # Vérifier que l'utilisateur est bien le conducteur du trajet
    if request.user != reservation.trajet.conducteur:
        messages.error(request, "Vous n'êtes pas autorisé à gérer cette réservation.")
        return redirect('mes_trajets')
    
    action = request.POST.get('action')
    if action == 'accepter':
        if reservation.trajet.places_disponibles < 1:
            messages.error(request, "Désolé, il n'y a plus de places disponibles.")
            return redirect('mes_trajets')
        
        reservation.statut = 'acceptee'
        reservation.trajet.places_disponibles -= 1
        reservation.trajet.save()
        reservation.save()
        
        # Envoyer une notification au passager
        notifier_statut_reservation(reservation, 'acceptee')
        
        # Programmer un rappel 1h avant le trajet
        heure_trajet = datetime.combine(reservation.trajet.date, reservation.trajet.heure_depart)
        heure_rappel = heure_trajet - timedelta(hours=1)
        if heure_rappel > timezone.now():
            notifier_rappel_trajet(reservation)
            
    elif action == 'refuser':
        reservation.statut = 'refusee'
        reservation.save()
        
        # Envoyer une notification au passager
        notifier_statut_reservation(reservation, 'refusee')
    
    return redirect('mes_trajets')

@login_required
def annuler_trajet(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id)
    
    # Vérifier que l'utilisateur est autorisé à annuler ce trajet
    if not (request.user == trajet.conducteur if hasattr(trajet, 'conducteur') else request.user == trajet.passager):
        messages.error(request, "Vous n'êtes pas autorisé à annuler ce trajet.")
        return redirect('mes_trajets')
    
    raison = request.POST.get('raison')
    trajet.statut = 'annule'
    trajet.save()
    
    # Envoyer des notifications aux personnes concernées
    notifier_annulation_trajet(trajet, raison)
    
    messages.success(request, "Le trajet a été annulé avec succès.")
    return redirect('mes_trajets')
