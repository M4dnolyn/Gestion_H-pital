from django.db import models
from personnes.models import Patient, Personnel
from planning.models import RendezVous

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    medecin = models.ForeignKey(
        Personnel,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'fonction': 'MED'},
        related_name='consultations'
    )
    date_consultation = models.DateField()
    heure_consultation = models.TimeField()
    diagnostic = models.TextField()
    observations_cliniques = models.TextField(blank=True)
    
    # Optionnel : lien avec le rendez-vous
    rendezvous = models.OneToOneField(
        RendezVous,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consultation'
    )
    
    def __str__(self):
        return f"Consultation {self.date_consultation} - {self.patient}"

class Ordonnance(models.Model):
    consultation = models.OneToOneField(
        Consultation,
        on_delete=models.CASCADE,
        related_name='ordonnance'
    )
    date_prescription = models.DateField(auto_now_add=True)
    contenu_medical = models.TextField()
    
    def __str__(self):
        return f"Ordonnance {self.date_prescription}"
