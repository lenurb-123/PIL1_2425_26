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
from django.contrib import messages

from .models import Discussion, Message
from .forms import MessageForm, GroupeCreationForm
from comptes.models import Utilisateur

from django.shortcuts import get_object_or_404
from .models import Discussion

@login_required
@csrf_exempt  # temporairement pour debug, à retirer après !
def conversation(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id, participants=request.user)

    # Déduire l'autre utilisateur dans une discussion privée
    if discussion.type == 'privee':
        other_user = discussion.participants.exclude(id=request.user.id).first()
    else:
        other_user = None

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.discussion = discussion
            message.expediteur = request.user
            
            # Gestion des médias
            if 'media' in request.FILES:
                media_file = request.FILES['media']
                # Déterminer le type de média
                content_type = media_file.content_type
                if content_type.startswith('image/'):
                    message.media_type = 'image'
                elif content_type.startswith('video/'):
                    message.media_type = 'video'
                elif content_type.startswith('audio/'):
                    message.media_type = 'audio'
                else:
                    message.media_type = 'document'
                
                # Sauvegarder le fichier
                path = default_storage.save(f'messages/{discussion.id}/{media_file.name}', ContentFile(media_file.read()))
                message.media = path

            message.save()
            
            # Marquer les messages comme lus
            discussion.marquer_messages_comme_lus(request.user)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': {
                        'id': message.id,
                        'contenu': message.contenu,
                        'media_url': message.media.url if message.media else None,
                        'media_type': message.media_type,
                        'date_envoi': message.date_envoi.strftime('%H:%M'),
                        'expediteur': message.expediteur.nom
                    }
                })
            return redirect('conversation', discussion_id=discussion.id)
        else:
            print('Form errors:', form.errors)  # Ajoute ceci pour voir les erreurs dans la console Django
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    # Récupérer les messages
    messages = discussion.messages.all().order_by('date_envoi')
    
    # Marquer les messages comme lus
    discussion.marquer_messages_comme_lus(request.user)

    context = {
        'discussion': discussion,
        'other_user': other_user,
        'messages': messages,
        'form': MessageForm()
    }
    return render(request, 'discussions/chat.html', context)



from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification  # adapte selon ton modèle

@login_required
def demarrer_discussion(request, user_id):
    destinataire = get_object_or_404(Utilisateur, pk=user_id)

    # Vérifier si une discussion privée existe déjà
    discussion_existante = Discussion.objects.filter(
        participants=request.user
    ).filter(participants=destinataire, type='privee').first()

    if discussion_existante:
        return redirect('conversation', discussion_id=discussion_existante.id)

    # Créer une nouvelle discussion privée
    nouvelle_discussion = Discussion.objects.create(
        type='privee',
        nom=f"Chat avec {destinataire.nom}"
    )
    nouvelle_discussion.participants.add(request.user, destinataire)
    return redirect('conversation', discussion_id=nouvelle_discussion.id)


@login_required
def creer_groupe(request):
    if request.method == 'POST':
        form = GroupeCreationForm(request.POST, request.FILES)
        if form.is_valid():
            groupe = form.save(commit=False)
            groupe.type = 'groupe'
            groupe.save()
            form.save_m2m()
            groupe.participants.add(request.user)  # Ajoute le créateur au groupe
            return redirect('conversation', discussion_id=groupe.id)
    else:
        form = GroupeCreationForm()
    return render(request, 'discussions/creer_groupe.html', {'form': form})


@login_required
def groupe_conversation(request, groupe_id):
    groupe = get_object_or_404(Discussion, id=groupe_id, type='groupe')
    messages = groupe.messages.order_by('date_envoie')
    return render(request, 'discussions/groupe_conversation.html', {
        'groupe': groupe,
        'messages': messages
    })


@login_required
def liste_utilisateurs(request):
    utilisateurs = Utilisateur.objects.exclude(id=request.user.id)
    return render(request, 'comptes/liste_utilisateurs.html', {
        'utilisateurs': utilisateurs
    })


@login_required
def discussion_detail(request, user_id):
    utilisateur = get_object_or_404(Utilisateur, id=user_id)
    return render(request, 'discussions/discussion_detail.html', {
        'utilisateur': utilisateur
    })


# discussions/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Discussion

@login_required
def liste_discussions(request):
    """Vue pour afficher la liste des discussions de l'utilisateur"""
    discussions = Discussion.objects.filter(
        participants=request.user
    ).prefetch_related(
        'participants',
        'messages'
    ).order_by('-date_modification')

    context = {
        'discussions': discussions,
        'today': timezone.now().date(),
    }
    return render(request, 'discussions/liste_discussions.html', context)

@login_required
def nouvelle_discussion(request):
    # Affiche un formulaire ou une page pour démarrer une nouvelle discussion
    return render(request, 'discussions/nouvelle_discussion.html')

@login_required
def recherche_utilisateurs(request):
    print("Recherche utilisateurs appelée")  # Debug log
    query = request.GET.get('q', '').strip()
    print(f"Query reçue: {query}")  # Debug log
    results = []
    if query:
        utilisateurs = Utilisateur.objects.filter(
            Q(nom__icontains=query) | Q(prenom__icontains=query) | Q(email__icontains=query)
        ).exclude(id=request.user.id)[:10]
        print(f"Utilisateurs trouvés: {utilisateurs.count()}")  # Debug log
        for u in utilisateurs:
            results.append({
                'id': u.id,
                'nom': f"{u.prenom} {u.nom}",
                'avatar': u.photo_profil.url if u.photo_profil else '/static/images/default-avatar.png',
                'email': u.email,
            })
    print(f"Résultats envoyés: {results}")  # Debug log
    return JsonResponse({'utilisateurs': results})

@login_required
def historique_discussion(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id, participants=request.user)
    messages = discussion.messages.order_by('date_envoi')
    return render(request, 'discussions/historique.html', {
        'discussion': discussion,
        'messages': messages
    })

@login_required
def nouvelle_conversation(request):
    if request.method == 'POST':
        destinataire_id = request.POST.get('destinataire')
        try:
            destinataire = Utilisateur.objects.get(id=destinataire_id)
            # Vérifier si une discussion existe déjà
            discussion = Discussion.objects.filter(
                type='privee',
                participants=request.user
            ).filter(
                participants=destinataire
            ).first()
            
            if not discussion:
                # Créer une nouvelle discussion
                discussion = Discussion.objects.create(type='privee')
                discussion.participants.add(request.user, destinataire)
            
            return redirect('conversation', discussion_id=discussion.id)
        except Utilisateur.DoesNotExist:
            messages.error(request, "Utilisateur non trouvé.")
            return redirect('nouvelle_conversation')
    
    # Récupérer tous les utilisateurs sauf soi-même
    utilisateurs = Utilisateur.objects.exclude(id=request.user.id)
    return render(request, 'discussions/nouvelle_conversation.html', {
        'utilisateurs': utilisateurs
    })