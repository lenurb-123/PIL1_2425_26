# trajets/utils.py

from datetime import timedelta, datetime, time
from comptes.utils import send_notification
from comptes.models import Utilisateur
from django.db.models import Q
from django.utils import timezone

def calculer_score_matching(trajet, demande):
    score = 0

    # 1. Proximité géographique (texte, inclusivité)
    if demande.lieu_depart.strip().lower() in trajet.lieu_depart.strip().lower() or trajet.lieu_depart.strip().lower() in demande.lieu_depart.strip().lower():
        score += 30
    if demande.lieu_arrivee.strip().lower() in trajet.lieu_arrivee.strip().lower() or trajet.lieu_arrivee.strip().lower() in demande.lieu_arrivee.strip().lower():
        score += 30

    # 2. Compatibilité horaire (±30 minutes autorisées) - protection maximale
    try:
        heure_trajet = getattr(trajet, 'heure_depart', None)
        heure_demande = getattr(demande, 'heure_souhaitee', None)
        if (
            heure_trajet is not None and isinstance(heure_trajet, time)
            and heure_demande is not None and isinstance(heure_demande, time)
        ):
            delta = abs(datetime.combine(datetime.today(), heure_trajet) -
                        datetime.combine(datetime.today(), heure_demande))
            if delta <= timedelta(minutes=15):
                score += 30
            elif delta <= timedelta(minutes=30):
                score += 15
    except TypeError:
        pass  # Ignore toute erreur de type
    except Exception:
        pass  # Ignore tout autre erreur

    # 3. Jours en commun
    jours_trajet = set(trajet.jours_semaine.split(',')) if getattr(trajet, 'jours_semaine', None) else set()
    jours_demande = set(demande.jours_semaine.split(',')) if getattr(demande, 'jours_semaine', None) else set()
    score += len(jours_trajet & jours_demande) * 5
    return round(score, 2)

def notifier_nouveau_trajet(trajet, type_trajet):
    """
    Envoie des notifications aux utilisateurs potentiellement intéressés par un nouveau trajet.
    
    Args:
        trajet: Instance de TrajetTaxi ou TrajetPassage
        type_trajet: 'conducteur' ou 'passager'
    """
    if type_trajet == 'conducteur':
        # Notifier les passagers qui cherchent un trajet dans la même zone
        utilisateurs_interesses = Utilisateur.objects.filter(
            role='passager',
            trajetpassage__lieu_depart__icontains=trajet.lieu_depart,
            trajetpassage__lieu_arrivee__icontains=trajet.lieu_arrivee,
        ).distinct()

        for utilisateur in utilisateurs_interesses:
            send_notification(
                user=utilisateur,
                type_notif='trajet',
                titre='Nouveau trajet disponible !',
                message=f'Un conducteur propose un trajet de {trajet.lieu_depart} à {trajet.lieu_arrivee} à {trajet.heure_depart.strftime("%H:%M")}',
                lien=f'/trajets/details/{trajet.id}/'
            )
    
    else:  # type_trajet == 'passager'
        # Notifier les conducteurs qui proposent des trajets dans la même zone
        utilisateurs_interesses = Utilisateur.objects.filter(
            role='conducteur',
            trajettaxi__lieu_depart__icontains=trajet.lieu_depart,
            trajettaxi__lieu_arrivee__icontains=trajet.lieu_arrivee,
        ).distinct()

        for utilisateur in utilisateurs_interesses:
            send_notification(
                user=utilisateur,
                type_notif='trajet',
                titre='Nouveau passager !',
                message=f'Un passager cherche un trajet de {trajet.lieu_depart} à {trajet.lieu_arrivee} à {trajet.heure_souhaitee.strftime("%H:%M")}',
                lien=f'/trajets/details/{trajet.id}/'
            )

def notifier_reservation(reservation):
    """
    Envoie des notifications pour une nouvelle réservation de trajet.
    """
    # Notifier le conducteur
    send_notification(
        user=reservation.trajet.conducteur,
        type_notif='reservation',
        titre='Nouvelle réservation',
        message=f'{reservation.passager.get_full_name()} souhaite réserver une place pour votre trajet vers {reservation.trajet.lieu_arrivee}',
        lien=f'/trajets/reservations/{reservation.id}/'
    )

def notifier_statut_reservation(reservation, nouveau_statut):
    """
    Envoie des notifications lors du changement de statut d'une réservation.
    """
    if nouveau_statut == 'acceptee':
        # Notifier le passager que sa réservation est acceptée
        send_notification(
            user=reservation.passager,
            type_notif='reservation_acceptee',
            titre='Réservation acceptée !',
            message=f'Votre réservation pour le trajet vers {reservation.trajet.lieu_arrivee} a été acceptée',
            lien=f'/trajets/reservations/{reservation.id}/'
        )
    
    elif nouveau_statut == 'refusee':
        # Notifier le passager que sa réservation est refusée
        send_notification(
            user=reservation.passager,
            type_notif='reservation_refusee',
            titre='Réservation refusée',
            message=f'Votre réservation pour le trajet vers {reservation.trajet.lieu_arrivee} a été refusée',
            lien=f'/trajets/rechercher/'
        )

def notifier_rappel_trajet(reservation):
    """
    Envoie des notifications de rappel avant un trajet.
    """
    # Rappel 1 heure avant le trajet
    message_conducteur = f"Rappel : Vous avez un trajet prévu dans 1 heure vers {reservation.trajet.lieu_arrivee} avec {reservation.passager.get_full_name()}"
    message_passager = f"Rappel : Vous avez un trajet prévu dans 1 heure vers {reservation.trajet.lieu_arrivee} avec {reservation.trajet.conducteur.get_full_name()}"

    # Notifier le conducteur
    send_notification(
        user=reservation.trajet.conducteur,
        type_notif='rappel_trajet',
        titre='Rappel de trajet',
        message=message_conducteur,
        lien=f'/trajets/details/{reservation.trajet.id}/'
    )

    # Notifier le passager
    send_notification(
        user=reservation.passager,
        type_notif='rappel_trajet',
        titre='Rappel de trajet',
        message=message_passager,
        lien=f'/trajets/details/{reservation.trajet.id}/'
    )

def notifier_annulation_trajet(trajet, raison=None):
    """
    Envoie des notifications en cas d'annulation d'un trajet.
    """
    message_base = f"Le trajet vers {trajet.lieu_arrivee} a été annulé"
    if raison:
        message_base += f" : {raison}"

    # Si c'est un trajet conducteur, notifier tous les passagers qui ont réservé
    if hasattr(trajet, 'reservations'):
        for reservation in trajet.reservations.all():
            send_notification(
                user=reservation.passager,
                type_notif='trajet_annule',
                titre='Trajet annulé',
                message=message_base,
                lien='/trajets/rechercher/'
            )
    
    # Si c'est une demande de trajet (passager), notifier le conducteur s'il y en a un
    elif hasattr(trajet, 'conducteur') and trajet.conducteur:
        send_notification(
            user=trajet.conducteur,
            type_notif='trajet_annule',
            titre='Trajet annulé',
            message=message_base,
            lien='/trajets/rechercher/'
        )
