# Imports Django utiles
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import email

# Utilitaires
from datetime import datetime, timedelta
import random
import json

# Modèles internes
from .models import Utilisateur, Notification, Newsletter, Conversation, Participant, ChatMessage
from trajets.models import TrajetTaxi, TrajetPassage

# Autres apps
from discussions.models import Message as DiscussionMessage, Discussion

# New imports
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import re
import qrcode
import io
import base64
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files import File
from qrcode.image.svg import SvgImage
from .forms import (
    UtilisateurCreationForm,
    UtilisateurChangeForm,
    ChangePasswordForm,
    ConnexionForm
)
from io import BytesIO

@login_required
def setup_2fa(request):
    """Vue pour configurer l'authentification à deux facteurs"""
    if request.method == 'POST':
        token = request.POST.get('token')
        
        # Vérification du token pour activer 2FA
        if not request.user.two_factor_enabled:
            if not request.user.totp_secret:
                request.user.enable_2fa()
            
            if request.user.verify_totp(token):
                request.user.two_factor_enabled = True
                request.user.save()
                messages.success(request, "L'authentification à deux facteurs a été activée avec succès!")
                return redirect('parametres')
            else:
                messages.error(request, "Code incorrect. Veuillez réessayer.")
    
    # Générer le QR code si 2FA n'est pas encore activé
    qr_code = None
    if not request.user.two_factor_enabled:
        if not request.user.totp_secret:
            request.user.enable_2fa()
        
        # Générer le QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(request.user.get_totp_uri())
        qr.make(fit=True)
        
        # Créer une image SVG du QR code
        img = qr.make_image(image_factory=SvgImage)
        buffer = BytesIO()
        img.save(buffer)
        qr_code = buffer.getvalue().decode()
    
    return render(request, 'comptes/setup_2fa.html', {
        'qr_code': qr_code,
        'secret_key': request.user.totp_secret
    })

@login_required
def verify_2fa(request):
    """Vue pour vérifier le code 2FA lors de la connexion"""
    if not request.user.two_factor_enabled:
        return redirect('accueil')
    
    if request.method == 'POST':
        token = request.POST.get('token')
        if request.user.verify_totp(token):
            request.session['2fa_verified'] = True
            return redirect(request.session.get('next', 'accueil'))
        else:
            messages.error(request, "Code incorrect. Veuillez réessayer.")
    
    return render(request, 'comptes/verify_2fa.html')

@login_required
def disable_2fa(request):
    """Vue pour désactiver l'authentification à deux facteurs"""
    if request.method == 'POST':
        request.user.disable_2fa()
        messages.success(request, "L'authentification à deux facteurs a été désactivée.")
        return redirect('parametres')
    return redirect('parametres')

# ------------------- INSCRIPTION -------------------
def recherche_utilisateur(request):
    q = request.GET.get('q', '')
    User = get_user_model()
    utilisateurs = User.objects.filter(
        Q(nom__icontains=q) | Q(prenom__icontains=q) 
    ).exclude(id=request.user.id)[:10]
    data = {
        'utilisateurs': [
            {'id': u.id, 'nom': u.get_full_name() or u.prenom}
            for u in utilisateurs
        ]
    }
    return JsonResponse(data)

@login_required
def supprimer_toutes_notifications(request):
    if request.method == "POST":
        Notification.objects.filter(utilisateur=request.user).delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def inscription(request):
    if request.method == 'POST':
        form = UtilisateurCreationForm(request.POST, request.FILES)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            utilisateur.set_password(form.cleaned_data['password'])
            utilisateur.is_active = True
            if 'photo_profil' in request.FILES:
                utilisateur.photo_profil = request.FILES['photo_profil']
            utilisateur.save()
            messages.success(request, "Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter.")
            return redirect('connexion')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = UtilisateurCreationForm()
    
    return render(request, 'comptes/inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            user = authenticate(request, email=email, password=mot_de_passe)

            if user:
                if user.deux_facteurs_active:
                    request.session['user_id'] = user.id
                    verify_2fa(user)
                    return redirect('verification_2fa')
                else:
                    login(request, user)

                    # 🔹 GESTION DU "SE SOUVENIR DE MOI"
                    if not request.POST.get('remember'):
                        # Expire à la fermeture du navigateur
                        request.session.set_expiry(0)
                    else:
                        # Expire dans 30 jours (par exemple)
                        request.session.set_expiry(30 * 24 * 60 * 60)

                    return render(request, 'comptes/parametres.html')

            else:
                messages.error(request, "Email ou mot de passe incorrect.")
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = ConnexionForm()

    return render(request, 'comptes/connexion.html', {'form': form})

# ------------------- DECONNEXION -------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('connexion')

# ------------------- PAGE D'ACCUEIL / LISTE DES UTILISATEURS -------------------
@login_required
def liste_utilisateurs(request):
    utilisateurs = Utilisateur.objects.exclude(id=request.user.id)
    return render(request, 'comptes/liste_utilisateurs.html', {'utilisateurs': utilisateurs})

def home(request):
    return render(request, 'comptes/accueil.html')

@login_required
def profil(request):
    user = request.user
    if request.method == 'POST':
        form = UtilisateurChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if 'photo_profil' in request.FILES:
                user.photo_profil = request.FILES['photo_profil']
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('profil')
    else:
        form = UtilisateurChangeForm(instance=user)
    return render(request, 'comptes/profil.html', {'form': form, 'user': user, 'deux_facteurs_active': user.deux_facteurs_active})

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user, lu=False)
    return JsonResponse({
        'notifications': list(notifications.values('id', 'type', 'titre', 'message', 'date_creation', 'lien'))
    })

@login_required
def marquer_notification_lue(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.lu = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)

def newsletter_inscription(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                Newsletter.objects.create(email=email)
                messages.success(request, "Inscription à la newsletter réussie !")
            except:
                messages.info(request, "Vous êtes déjà inscrit à la newsletter.")
        else:
            messages.error(request, "Veuillez fournir une adresse email valide.")
    return redirect('accueil')

def creer_notification(user, type_notif, titre, message, lien=None):
    """Fonction utilitaire pour créer une notification"""
    return Notification.objects.create(
        user=user,
        type=type_notif,
        titre=titre,
        message=message,
        lien=lien
    )

@login_required
def publier_trajet(request):
    """Vue pour la publication d'un nouveau trajet."""
    return render(request, 'comptes/publier_trajet.html')

def contact(request):
    """Vue pour la page de contact."""
    return render(request, 'comptes/contact.html')

@login_required
def messagerie(request):
    return render(request, 'comptes/messagerie.html')

def infos(request):
    return render(request, 'comptes/infos.html')


@login_required
@require_http_methods(['GET'])
def get_conversations(request):
    conversations = Conversation.objects.filter(participants__user=request.user).order_by('-updated_at')
    data = [{
        'id': conv.id,
        'type': conv.type,
        'name': conv.name,
        'last_message': conv.messages.last().content if conv.messages.exists() else '',
        'updated_at': conv.updated_at.strftime('%H:%M'),
        'unread_count': conv.messages.filter(is_read=False).exclude(sender=request.user).count()
    } for conv in conversations]
    return JsonResponse({'conversations': data})

@login_required
@require_http_methods(['GET'])
def get_messages(request, conversation_id):
    conversation = Conversation.objects.get(id=conversation_id, participants__user=request.user)
    messages = conversation.messages.all().order_by('created_at')
    data = [{
        'id': msg.id,
        'sender': msg.sender.username,
        'content': msg.content,
        'created_at': msg.created_at.strftime('%H:%M'),
        'is_sent': msg.sender == request.user
    } for msg in messages]
    return JsonResponse({'messages': data})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime

from .models import  Message

from comptes.models import Utilisateur


# ... rest of the existing views ...
@login_required
@require_http_methods(['POST'])
def send_message(request, conversation_id):
    data = json.loads(request.body)
    conversation = Conversation.objects.get(id=conversation_id, participants__user=request.user)
    message = ChatMessage.objects.create(
        conversation=conversation,
        sender=request.user,
        content=data['content']
    )
    return JsonResponse({
        'id': message.id,
        'sender': message.sender.username,
        'content': message.content,
        'created_at': message.created_at.strftime('%H:%M'),
        'is_sent': True
    })

@login_required
@require_http_methods(['POST'])
def create_conversation(request):
    data = json.loads(request.body)
    conversation = Conversation.objects.create(
        type=data['type'],
        name=data.get('name', '')
    )
    Participant.objects.create(
        conversation=conversation,
        user=request.user,
        is_admin=True
    )
    for user_id in data['participants']:
        Participant.objects.create(
            conversation=conversation,
            user_id=user_id
        )
    return JsonResponse({
        'id': conversation.id,
        'type': conversation.type,
        'name': conversation.name
    })

@login_required
def mes_trajets(request):
    trajets_publies = TrajetTaxi.objects.filter(conducteur=request.user).order_by('-date_creation')
    trajets_reserves = TrajetPassage.objects.filter(passager=request.user).order_by('-date_creation')
    
    context = {
        'trajets_publies': trajets_publies,
        'trajets_reserves': trajets_reserves,
    }
    return render(request, 'comptes/mes_trajets.html', context)

@login_required
def discussions(request):
    discussions = Discussion.objects.filter(participants=request.user).order_by('-date_modification')
    return render(request, 'comptes/discussions.html', {'discussions': discussions})

@login_required
def parametres(request):
    user = request.user
    form = UtilisateurChangeForm(instance=user)
    password_form = ChangePasswordForm(user)

    if request.method == 'POST':
        # Gestion de la suppression de photo
        if 'delete_photo' in request.POST:
            user.photo_profil.delete(save=False)
            user.photo_profil = None
            user.save()
            messages.success(request, "Photo de profil supprimée.")
            return redirect('parametres')
        
        # Gestion du changement de mot de passe
        if 'change_password' in request.POST:
            password_form = ChangePasswordForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, "Votre mot de passe a été modifié avec succès. Veuillez vous reconnecter.")
                return redirect('connexion')
            else:
                messages.error(request, "Erreur dans le changement de mot de passe.")
        else:
            # Gestion de la mise à jour du profil
            form = UtilisateurChangeForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profil mis à jour avec succès.")
                return redirect('parametres')
    
    return render(request, 'comptes/parametres.html', {
        'form': form,
        'password_form': password_form,
        'user': user
    })

@login_required
def payment(request):
    """Vue pour la page de paiement."""
    # Récupérer les paramètres de l'URL
    depart = request.GET.get('depart', '')
    arrivee = request.GET.get('arrivee', '')
    tarif = request.GET.get('tarif', '0')
    type_trajet = request.GET.get('type', '')
    trajet_id = request.GET.get('trajet_id', '')
    
    context = {
        'depart': depart,
        'arrivee': arrivee,
        'tarif': tarif,
        'type_trajet': type_trajet,
        'trajet_id': trajet_id,
    }
    
    return render(request, 'comptes/payment.html', context)

@login_required
def debug_notifications(request):
    """Vue de debug pour afficher toutes les notifications"""
    notifications = Notification.objects.all().order_by('-date_creation')
    return render(request, 'comptes/debug_notifications.html', {
        'notifications': notifications
    })