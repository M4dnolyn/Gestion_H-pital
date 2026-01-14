from django.db import models
from personnes.models import Personnel

class Service(models.Model):
    nom_service = models.CharField(max_length=100)
    localisation = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    responsable = models.ForeignKey(
        Personnel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'fonction': 'RES'},
        related_name='services_diriges'
    )
    
    def __str__(self):
        return self.nom_service
