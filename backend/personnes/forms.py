from django import forms
from .models import Patient, Personnel, ProcheAidant


class PatientForm(forms.ModelForm):
    """Formulaire pour créer/modifier un patient"""
    
    class Meta:
        model = Patient
        fields = [
            'nom', 'prenom', 'date_naissance', 'sexe',
            'adresse', 'telephone', 'email',
            'groupe_sanguin', 'assurance', 'antecedent'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sexe': forms.Select(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+221 XX XXX XX XX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'groupe_sanguin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A+, B-, O+, etc.'}),
            'assurance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'assurance'}),
            'antecedent': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Antécédents médicaux'}),
        }
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'date_naissance': 'Date de naissance',
            'sexe': 'Sexe',
            'adresse': 'Adresse',
            'telephone': 'Téléphone',
            'email': 'Email',
            'groupe_sanguin': 'Groupe sanguin',
            'assurance': 'Assurance',
            'antecedent': 'Antécédents médicaux',
        }


class PersonnelForm(forms.ModelForm):
    """Formulaire pour créer/modifier un membre du personnel"""
    
    class Meta:
        model = Personnel
        fields = [
            'nom', 'prenom', 'date_naissance', 'sexe',
            'adresse', 'telephone', 'email',
            'fonction', 'specialite', 'statut', 'date_embauche'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sexe': forms.Select(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'fonction': forms.Select(attrs={'class': 'form-control'}),
            'specialite': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Cardiologie, Pédiatrie...'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'date_embauche': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ProcheAidantForm(forms.ModelForm):
    """Formulaire pour créer/modifier un proche aidant"""
    
    class Meta:
        model = ProcheAidant
        fields = ['nom', 'prenom', 'lien_parent', 'telephone', 'date_naissance', 'patients']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'lien_parent': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Père, Mère, Conjoint...'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'patients': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5'}),
        }
