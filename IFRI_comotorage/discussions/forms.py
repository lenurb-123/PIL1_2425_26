# discussions/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Message, Discussion  # Importer les modèles, pas les forms

User = get_user_model()

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['contenu', 'media']
        widgets = {
            'contenu': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tapez un message...'
            }),
            'media': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': ','.join(
                    settings.ALLOWED_IMAGE_TYPES +
                    settings.ALLOWED_VIDEO_TYPES +
                    settings.ALLOWED_AUDIO_TYPES +
                    settings.ALLOWED_DOCUMENT_TYPES
                )
            })
        }

    def clean_media(self):
        media = self.cleaned_data.get('media')
        if media:
            content_type = media.content_type
            if (content_type not in settings.ALLOWED_IMAGE_TYPES and
                content_type not in settings.ALLOWED_VIDEO_TYPES and
                content_type not in settings.ALLOWED_AUDIO_TYPES and
                content_type not in settings.ALLOWED_DOCUMENT_TYPES):
                raise forms.ValidationError('Type de fichier non autorisé.')
            
            if media.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
                raise forms.ValidationError('Le fichier est trop volumineux. Taille maximale : 10MB.')
        return media

class GroupeCreationForm(forms.ModelForm):
    """Formulaire pour créer une nouvelle discussion/groupe"""
    
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Participants"
    )
    
    class Meta:
        model = Discussion
        fields = ['nom', 'description', 'photo', 'participants']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': ','.join(settings.ALLOWED_IMAGE_TYPES)
            }),
            'participants': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
        
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            if photo.content_type not in settings.ALLOWED_IMAGE_TYPES:
                raise forms.ValidationError('Type d\'image non autorisé.')
            if photo.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
                raise forms.ValidationError('L\'image est trop volumineuse. Taille maximale : 10MB.')
        return photo

    def __init__(self, *args, **kwargs):
        # Exclure l'utilisateur actuel des participants sélectionnables
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        
        if self.current_user:
            self.fields['participants'].queryset = User.objects.exclude(
                id=self.current_user.id
            )

# Alternative si vous voulez un formulaire plus personnalisé
class GroupeCreationFormCustom(forms.Form):
    """Formulaire personnalisé pour créer un groupe"""
    
    nom = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom du groupe (optionnel)'
        })
    )
    
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=True,
        label="Sélectionner les participants"
    )
    
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        
        if self.current_user:
            self.fields['participants'].queryset = User.objects.exclude(
                id=self.current_user.id
            )
    
    def save(self, current_user):
        """Créer la discussion avec les participants sélectionnés"""
        participants = self.cleaned_data['participants']
        
        # Créer la discussion
        discussion = Discussion.objects.create()
        
        # Ajouter le créateur et les participants
        discussion.participants.add(current_user)
        discussion.participants.add(*participants)
        
        return discussion