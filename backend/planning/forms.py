from django import forms
from .models import RendezVous
from personnes.models import Patient, Personnel


class RendezVousForm(forms.ModelForm):
    """Formulaire pour créer/modifier un rendez-vous"""
    
    class Meta:
        model = RendezVous
        fields = ['patient', 'medecin', 'date_rdv', 'heure_rdv', 'motif', 'statut_rdv']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'medecin': forms.Select(attrs={'class': 'form-control'}),
            'date_rdv': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'heure_rdv': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'motif': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Motif de la consultation'}),
            'statut_rdv': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'patient': 'Patient',
            'medecin': 'Médecin',
            'date_rdv': 'Date du rendez-vous',
            'heure_rdv': 'Heure du rendez-vous',
            'motif': 'Motif',
            'statut_rdv': 'Statut',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer pour n'afficher que les médecins
        self.fields['medecin'].queryset = Personnel.objects.filter(fonction='MED')
        self.fields['medecin'].label_from_instance = lambda obj: f"Dr. {obj.nom} {obj.prenom}"
