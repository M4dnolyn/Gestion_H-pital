from django import forms
from .models import Service
from personnes.models import Personnel


class ServiceForm(forms.ModelForm):
    """Formulaire pour créer/modifier un service"""
    
    class Meta:
        model = Service
        fields = ['nom_service', 'localisation', 'description', 'responsable']
        widgets = {
            'nom_service': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Cardiologie, Urgences, Pédiatrie...'
            }),
            'localisation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Bâtiment A - 2ème étage'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Description du service...'
            }),
            'responsable': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nom_service': 'Nom du service',
            'localisation': 'Localisation',
            'description': 'Description',
            'responsable': 'Responsable du service',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer pour n'afficher que les responsables de service
        self.fields['responsable'].queryset = Personnel.objects.filter(fonction='RES')
        self.fields['responsable'].required = False
