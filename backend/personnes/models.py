# personnes/models.py
from django.db import models
from django.conf import settings  # IMPORTANT
from core.models import Personne

class Patient(Personne):
    groupe_sanguin = models.CharField(max_length=5, blank=True)
    assurance = models.CharField(max_length=100, blank=True)
    date_inscription = models.DateField(auto_now_add=True)
    antecedent = models.TextField(blank=True)
    
    def __str__(self):
        return f"Patient: {self.nom_complet}"

class Personnel(Personne):
    FONCTIONS = [
        ('MED', 'Médecin'),
        ('INF', 'Infirmier'),
        ('ADM', 'Agent administratif'),
        ('CAI', 'Caissier'),
        ('RES', 'Responsable service'),
        ('DIR', 'Direction'),
        ('ADMIN', 'Administrateur système'),
    ]
    
    STATUTS = [
        ('ACT', 'Actif'),
        ('CON', 'En congé'),
        ('SUS', 'Suspendu'),
    ]
    
    # CORRECTION : Utiliser settings.AUTH_USER_MODEL
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='personnel_profile', 
        null=True, 
        blank=True
    )
    
    fonction = models.CharField(max_length=5, choices=FONCTIONS)
    specialite = models.CharField(max_length=100, blank=True, null=True)
    statut = models.CharField(max_length=3, choices=STATUTS, default='ACT')
    date_embauche = models.DateField()
    
    def __str__(self):
        return f"{self.get_fonction_display()}: {self.nom_complet}"

class ProcheAidant(models.Model):
    patients = models.ManyToManyField(Patient, related_name='proches')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    lien_parent = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)
    date_naissance = models.DateField()
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"

    def __str__(self):
        return self.nom_complet