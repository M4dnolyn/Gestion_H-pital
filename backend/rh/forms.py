from django import forms
from .models import Conge, PersonnelService
from personnes.models import Personnel
from services.models import Service


class CongeForm(forms.ModelForm):
    """Formulaire pour créer/modifier une demande de congé"""
    
    class Meta:
        model = Conge
        fields = ['personnel', 'date_debut', 'date_fin', 'type_conge', 'statut_conge']
        widgets = {
            'personnel': forms.Select(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'type_conge': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('Congé annuel', 'Congé annuel'),
                ('Congé maladie', 'Congé maladie'),
                ('Congé maternité', 'Congé maternité'),
                ('Congé paternité', 'Congé paternité'),
                ('Congé sans solde', 'Congé sans solde'),
                ('Autre', 'Autre'),
            ]),
            'statut_conge': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('En attente', 'En attente'),
                ('Approuvé', 'Approuvé'),
                ('Refusé', 'Refusé'),
            ]),
        }
        labels = {
            'personnel': 'Personnel',
            'date_debut': 'Date de début',
            'date_fin': 'Date de fin',
            'type_conge': 'Type de congé',
            'statut_conge': 'Statut',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        
        if date_debut and date_fin and date_debut > date_fin:
            raise forms.ValidationError("La date de début doit être antérieure à la date de fin.")
        
        return cleaned_data


class PersonnelServiceForm(forms.ModelForm):
    """Formulaire pour affecter un personnel à un service"""
    
    class Meta:
        model = PersonnelService
        fields = ['personnel', 'service']
        widgets = {
            'personnel': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'personnel': 'Personnel',
            'service': 'Service',
        }
