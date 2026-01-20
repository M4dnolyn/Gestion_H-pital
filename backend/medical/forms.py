from django import forms
from .models import Consultation, Ordonnance
from personnes.models import Patient, Personnel


class ConsultationForm(forms.ModelForm):
    """Formulaire pour créer/modifier une consultation"""
    
    class Meta:
        model = Consultation
        fields = [
            'patient', 'medecin', 'date_consultation', 'heure_consultation',
            'diagnostic', 'observations_cliniques', 'rendezvous'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'medecin': forms.Select(attrs={'class': 'form-control'}),
            'date_consultation': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'heure_consultation': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'diagnostic': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Diagnostic médical'}),
            'observations_cliniques': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observations cliniques'}),
            'rendezvous': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'patient': 'Patient',
            'medecin': 'Médecin',
            'date_consultation': 'Date de consultation',
            'heure_consultation': 'Heure de consultation',
            'diagnostic': 'Diagnostic',
            'observations_cliniques': 'Observations cliniques',
            'rendezvous': 'Rendez-vous associé (optionnel)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer pour n'afficher que les médecins
        self.fields['medecin'].queryset = Personnel.objects.filter(fonction='MED')
        self.fields['medecin'].label_from_instance = lambda obj: f"Dr. {obj.nom} {obj.prenom}"
        # Rendez-vous optionnel
        self.fields['rendezvous'].required = False


class OrdonnanceForm(forms.ModelForm):
    """Formulaire pour créer/modifier une ordonnance"""
    
    class Meta:
        model = Ordonnance
        fields = ['consultation', 'contenu_medical']
        widgets = {
            'consultation': forms.Select(attrs={'class': 'form-control'}),
            'contenu_medical': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Détails de l\'ordonnance (médicaments, posologie, durée...)'
            }),
        }
        labels = {
            'consultation': 'Consultation',
            'contenu_medical': 'Contenu de l\'ordonnance',
        }
