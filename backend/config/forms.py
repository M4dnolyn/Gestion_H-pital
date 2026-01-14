# forms.py
from django import forms
from .models import Patient, RendezVous, Consultation, Medecin

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'adresse': forms.Textarea(attrs={'rows': 3}),
            'antecedents': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'date_naissance': 'Date de naissance',
            'groupe_sanguin': 'Groupe sanguin',
            'antecedents': 'Antécédents médicaux',
            'allergies': 'Allergies connues',
        }

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'heure_debut': forms.TimeInput(attrs={'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'patient': 'Patient',
            'medecin': 'Médecin',
            'date': 'Date du rendez-vous',
            'heure_debut': 'Heure de début',
            'heure_fin': 'Heure de fin',
            'type': 'Type de rendez-vous',
            'statut': 'Statut',
            'notes': 'Notes',
        }

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'heure': forms.TimeInput(attrs={'type': 'time'}),
            'motif': forms.Textarea(attrs={'rows': 3}),
            'diagnostic': forms.Textarea(attrs={'rows': 3}),
            'observations': forms.Textarea(attrs={'rows': 3}),
            'traitement': forms.Textarea(attrs={'rows': 3}),
            'recommandations': forms.Textarea(attrs={'rows': 3}),
            'date_prochain_rdv': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'patient': 'Patient',
            'medecin': 'Médecin',
            'date': 'Date de consultation',
            'heure': 'Heure',
            'motif': 'Motif de consultation',
            'diagnostic': 'Diagnostic',
            'tension_arterielle': 'Tension artérielle',
            'poids': 'Poids (kg)',
            'taille': 'Taille (cm)',
            'temperature': 'Température (°C)',
            'observations': 'Observations cliniques',
            'traitement': 'Traitement prescrit',
            'ordonnance_requise': 'Ordonnance requise',
            'recommandations': 'Recommandations',
            'date_prochain_rdv': 'Date du prochain rendez-vous',
            'statut': 'Statut de la consultation',
        }
