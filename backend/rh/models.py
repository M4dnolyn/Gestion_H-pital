from django.db import models
from personnes.models import Personnel
from services.models import Service

class PersonnelService(models.Model):
    """Table d'association pour la relation ManyToMany Personnel-Service"""
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_affectation = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ['personnel', 'service']

class Conge(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name='conges')
    date_debut = models.DateField()
    date_fin = models.DateField()
    type_conge = models.CharField(max_length=50)
    statut_conge = models.CharField(max_length=50, default='En attente')
    
    def __str__(self):
        return f"Congé {self.type_conge} - {self.personnel}"
