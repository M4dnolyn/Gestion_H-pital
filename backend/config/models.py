from django.db import models
from django.contrib.auth.models import User
from datetime import date  # IMPORTANT : ajouter cette ligne
from django.conf import settings  # Ajoute en haut du fichier
class Patient(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre'),
    ]
    
    GROUPE_SANGUIN_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, default='M')
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    adresse = models.TextField(blank=True)
    
    # Informations médicales
    groupe_sanguin = models.CharField(max_length=3, choices=GROUPE_SANGUIN_CHOICES, blank=True)
    antecedents = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nom', 'prenom']
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
    def age(self):
        if self.date_naissance:
            today = date.today()
            return today.year - self.date_naissance.year - (
                (today.month, today.day) < (self.date_naissance.month, self.date_naissance.day)
            )
        return None


class Medecin(models.Model):
    SPECIALITE_CHOICES = [
        ('generaliste', 'Généraliste'),
        ('cardiologue', 'Cardiologue'),
        ('dermatologue', 'Dermatologue'),
        ('pediatre', 'Pédiatre'),
        ('gynecologue', 'Gynécologue'),
        ('autre', 'Autre'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medecin')
    specialite = models.CharField(max_length=50, choices=SPECIALITE_CHOICES, default='generaliste')
    telephone = models.CharField(max_length=20, blank=True)
    matricule = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"Dr. {self.user.last_name} {self.user.first_name}"


class RendezVous(models.Model):
    TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('suivi', 'Suivi'),
        ('urgence', 'Urgence'),
        ('autre', 'Autre'),
    ]
    
    STATUT_CHOICES = [
        ('en attente', 'En attente'),
        ('confirmé', 'Confirmé'),
        ('annulé', 'Annulé'),
        ('reporté', 'Reporté'),
        ('terminé', 'Terminé'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rendezvous')
    medecin = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, blank=True, related_name='rendezvous')
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='consultation')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en attente')
    notes = models.TextField(blank=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date', 'heure_debut']
        verbose_name_plural = "Rendez-vous"
    
    def __str__(self):
        return f"RDV {self.patient} - {self.date} {self.heure_debut}"


class Consultation(models.Model):
    STATUT_CHOICES = [
        ('planifiée', 'Planifiée'),
        ('en cours', 'En cours'),
        ('terminée', 'Terminée'),
        ('annulée', 'Annulée'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    medecin = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultations')
    date = models.DateField()
    heure = models.TimeField()
    
    # Motif et diagnostic
    motif = models.TextField()
    diagnostic = models.TextField(blank=True)
    
    # Examen clinique
    tension_arterielle = models.CharField(max_length=20, blank=True)
    poids = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    taille = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    observations = models.TextField(blank=True)
    
    # Traitement
    traitement = models.TextField(blank=True)
    ordonnance_requise = models.BooleanField(default=False)
    
    # Suivi
    recommandations = models.TextField(blank=True)
    date_prochain_rdv = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='terminée')
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-heure']
    
    def __str__(self):
        return f"Consultation {self.patient} - {self.date}"
    
    def imc(self):
        if self.poids and self.taille:
            taille_m = self.taille / 100
            return self.poids / (taille_m * taille_m)
        return None
