from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import Utilisateur
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re


from django import forms
from .models import Utilisateur

class UtilisateurCreationForm(forms.ModelForm):
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
        strip=False,
    )
    password_confirm = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput,
        strip=False,
    )
    photo_profil = forms.ImageField(
        label="Photo de profil",
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )

    class Meta:
        model = Utilisateur
        fields = ['email', 'nom', 'prenom', 'telephone', 'role', 'immatriculation', 'photo_profil']
    def clean(self):
        # Validation du mot de passe et de l'immatriculation pour les conducteurs
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password_confirm"):
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        if cleaned_data.get("role") == 'conducteur' and not cleaned_data.get("immatriculation"):
            raise forms.ValidationError("L'immatriculation est obligatoire pour les conducteurs.")
        return cleaned_data

    def save(self, commit=True):
        # Hachage du mot de passe avant sauvegarde
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UtilisateurChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Mot de passe (haché, non modifiable)")
    deux_facteurs_active = forms.BooleanField(label="Activer la double authentification (2FA)", required=False)
    photo_profil = forms.ImageField(
        label="Photo de profil",
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )

    class Meta:
        model = Utilisateur
        fields = (
            'email', 'prenom', 'nom', 'telephone', 'role', 'immatriculation', 'heure_arrivee_habituelle', 'heure_depart_habituelle', 'modele_vehicule', 'marque_vehicule', 'adresse_depart_habituelle', 'places_disponibles',
            'is_active', 'is_staff', 'is_superuser', 'deux_facteurs_active', 'photo_profil'
        )

    def clean_password(self):
        return self.initial.get("password", self.instance.password)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)
        qs = Utilisateur.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone.startswith('+'):
            if not re.match(r'^\+229\d{8}$', telephone):
                raise ValidationError("Numéro de téléphone invalide. Format attendu : +229XXXXXXXX.")
        else:
            if not re.match(r'^\d{8}$', telephone):
                raise ValidationError("Numéro de téléphone invalide. Format attendu : 8 chiffres ou +229XXXXXXXX.")
            telephone = '+229' + telephone
        qs = Utilisateur.objects.filter(telephone=telephone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Ce numéro de téléphone est déjà utilisé.")
        return telephone

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Mot de passe actuel",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label="Confirmer le nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Utilisateur
        fields = ['old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = "Mot de passe actuel"
        self.fields['new_password1'].label = "Nouveau mot de passe"
        self.fields['new_password2'].label = "Confirmer le nouveau mot de passe"

class ConnexionForm(forms.Form):
    email = forms.EmailField(label="Adresse e-mail")
    mot_de_passe = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
