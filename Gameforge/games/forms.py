from django import forms
from .models import Game


class GameCreationForm(forms.Form):
    """Formulaire pour créer un jeu avec l'IA"""
    
    genre = forms.ChoiceField(
        choices=Game.GENRE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    ambiance = forms.ChoiceField(
        choices=Game.AMBIANCE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    mots_cles = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: dragons, magie, château'
        }),
        help_text="Séparez les mots-clés par des virgules"
    )
    
    references = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Dark Souls, Zelda, Game of Thrones'
        }),
        help_text="Références culturelles optionnelles"
    )
    
    est_public = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Rendre le jeu public"
    )