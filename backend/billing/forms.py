from django import forms
from .models import Facture, Paiement, Prestation, FacturePrestation
from personnes.models import Patient


class PrestationForm(forms.ModelForm):
    """Formulaire pour créer/modifier une prestation"""
    
    class Meta:
        model = Prestation
        fields = ['libelle_acte', 'tarif_unitaire']
        widgets = {
            'libelle_acte': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Consultation générale, Radio, Analyse...'
            }),
            'tarif_unitaire': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
        }
        labels = {
            'libelle_acte': 'Libellé de l\'acte',
            'tarif_unitaire': 'Tarif unitaire (FCFA)',
        }


class FactureForm(forms.ModelForm):
    """Formulaire pour créer/modifier une facture"""
    
    class Meta:
        model = Facture
        fields = ['patient', 'statut_paiement']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'statut_paiement': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('En attente', 'En attente'),
                ('Payée', 'Payée'),
                ('Partiellement payée', 'Partiellement payée'),
                ('Annulée', 'Annulée'),
            ]),
        }
        labels = {
            'patient': 'Patient',
            'statut_paiement': 'Statut du paiement',
        }


class FacturePrestationForm(forms.ModelForm):
    """Formulaire pour ajouter une prestation à une facture"""
    
    class Meta:
        model = FacturePrestation
        fields = ['prestation', 'qte', 'prix_unit']
        widgets = {
            'prestation': forms.Select(attrs={'class': 'form-control'}),
            'qte': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
            'prix_unit': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Prix unitaire'
            }),
        }
        labels = {
            'prestation': 'Prestation',
            'qte': 'Quantité',
            'prix_unit': 'Prix unitaire',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Auto-remplir le prix unitaire depuis la prestation
        if 'prestation' in self.data:
            try:
                prestation_id = int(self.data.get('prestation'))
                prestation = Prestation.objects.get(id=prestation_id)
                self.fields['prix_unit'].initial = prestation.tarif_unitaire
            except (ValueError, Prestation.DoesNotExist):
                pass


class PaiementForm(forms.ModelForm):
    """Formulaire pour enregistrer un paiement"""
    
    class Meta:
        model = Paiement
        fields = ['facture', 'date_paiement', 'montant_paye', 'mode_paiement', 'reference']
        widgets = {
            'facture': forms.Select(attrs={'class': 'form-control'}),
            'date_paiement': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'montant_paye': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'mode_paiement': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('Espèces', 'Espèces'),
                ('Carte bancaire', 'Carte bancaire'),
                ('Chèque', 'Chèque'),
                ('Virement', 'Virement'),
                ('Mobile Money', 'Mobile Money'),
            ]),
            'reference': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro de référence du paiement'
            }),
        }
        labels = {
            'facture': 'Facture',
            'date_paiement': 'Date du paiement',
            'montant_paye': 'Montant payé (FCFA)',
            'mode_paiement': 'Mode de paiement',
            'reference': 'Référence',
        }
