from django.db import models

class Personne(models.Model):
    """Classe abstraite pour tous les individus"""
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    
    class Meta:
        abstract = True
        ordering = ['nom', 'prenom']
    
    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"
