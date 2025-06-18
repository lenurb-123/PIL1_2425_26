from django import forms
from .models import TrajetTaxi, TrajetPassage

# À placer dans un fichier constants.py ou au début si réutilisé ailleurs
JOURS_SEMAINE = [
    ('Lun', 'Lundi'),
    ('Mar', 'Mardi'),
    ('Mer', 'Mercredi'),
    ('Jeu', 'Jeudi'),
    ('Ven', 'Vendredi'),
    ('Sam', 'Samedi'),
    ('Dim', 'Dimanche'),
]

class RechercheTrajetForm(forms.Form):
    depart = forms.CharField(
        label="Lieu de départ",
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': "Ex : IFRI, Cotonou",
            'autocomplete': 'off',
            'id': 'lieu_depart_autocomplete',
        })
    )
    arrivee = forms.CharField(
        label="Lieu d'arrivée",
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': "Ex : IFRI, Cotonou",
            'autocomplete': 'off',
            'id': 'lieu_arrivee_autocomplete',
        })
    )

class TrajetConducteurForm(forms.ModelForm):
    jours = forms.MultipleChoiceField(
        choices=JOURS_SEMAINE,
        widget=forms.CheckboxSelectMultiple,
        label="Jours de disponibilité"
    )
    lieu_depart = forms.CharField(
        label="Lieu de départ",
        widget=forms.TextInput(attrs={
            'placeholder': "Ex : IFRI, Cotonou",
            'autocomplete': 'off',
            'id': 'lieu_depart_autocomplete',
        })
    )
    latitude_depart = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude_depart = forms.FloatField(widget=forms.HiddenInput(), required=False)
    lieu_arrivee = forms.CharField(
        label="Lieu d'arrivée",
        initial="IFRI UAC Bénin",
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = TrajetTaxi
        fields = [
            'lieu_depart', 'latitude_depart', 'longitude_depart',
            'lieu_arrivee', 'heure_depart', 'places_disponibles'
        ]

    def clean(self):
        cleaned_data = super().clean()
        jours = self.cleaned_data.get('jours')
        if not jours:
            raise forms.ValidationError("Veuillez sélectionner au moins un jour.")
        cleaned_data['jours_semaine'] = ','.join(jours)
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.jours_semaine = ','.join(self.cleaned_data['jours'])
        if commit:
            instance.save()
        return instance


class TrajetPassagerForm(forms.ModelForm):
    jours = forms.MultipleChoiceField(
        choices=JOURS_SEMAINE,
        widget=forms.CheckboxSelectMultiple,
        label="Jours souhaités"
    )
    lieu_depart = forms.CharField(
        label="Lieu de départ",
        widget=forms.TextInput(attrs={
            'placeholder': "Ex : IFRI, Cotonou",
            'autocomplete': 'off',
            'id': 'lieu_depart_autocomplete',
        })
    )
    latitude_depart = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude_depart = forms.FloatField(widget=forms.HiddenInput(), required=False)
    lieu_arrivee = forms.CharField(
        label="Lieu d'arrivée",
        initial="IFRI UAC Bénin",
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = TrajetPassage
        fields = [
            'lieu_depart', 'latitude_depart', 'longitude_depart',
            'lieu_arrivee', 'heure_souhaitee'
        ]

    def clean(self):
        cleaned_data = super().clean()
        jours = self.cleaned_data.get('jours')
        if not jours:
            raise forms.ValidationError("Veuillez sélectionner au moins un jour.")
        cleaned_data['jours_semaine'] = ','.join(jours)
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.jours_semaine = ','.join(self.cleaned_data['jours'])
        if commit:
            instance.save()
        return instance
