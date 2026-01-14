from django.db import models
from personnes.models import Patient, Personnel

class RendezVous(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rendezvous')
    medecin = models.ForeignKey(
        Personnel,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'fonction': 'MED'},
        related_name='rendezvous'
    )
    date_rdv = models.DateField()
    heure_rdv = models.TimeField()
    motif = models.TextField()
    statut_rdv = models.CharField(max_length=20, default='Programmé')
    
    def __str__(self):
        return f"RDV {self.date_rdv} - {self.patient}"
