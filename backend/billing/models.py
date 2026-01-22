from django.db import models


class Prestation(models.Model):
    libelle_acte = models.CharField(max_length=100)
    tarif_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.libelle_acte


class Facture(models.Model):
    patient = models.ForeignKey(
        'personnes.Patient',
        on_delete=models.CASCADE,
        related_name='factures'
    )
    date_facture = models.DateField(auto_now_add=True)
    statut_paiement = models.CharField(max_length=50)

    prestations = models.ManyToManyField(
        Prestation,
        through='FacturePrestation',
        related_name='factures'
    )

    def __str__(self):
        return f"Facture {self.id}"

    @property
    def get_total(self):
        """Calcule le total de la facture"""
        return sum(ligne.qte * ligne.prix_unit for ligne in self.lignes.all())


class FacturePrestation(models.Model):
    facture = models.ForeignKey(
        Facture,
        on_delete=models.CASCADE,
        related_name='lignes'
    )
    prestation = models.ForeignKey(
        Prestation,
        on_delete=models.CASCADE
    )
    qte = models.PositiveIntegerField()
    prix_unit = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_ligne(self):
        """Calcule le total de la ligne"""
        return self.qte * self.prix_unit

    def __str__(self):
        return f"{self.prestation} x {self.qte}"


class Paiement(models.Model):
    facture = models.OneToOneField(
        Facture,
        on_delete=models.CASCADE,
        related_name='paiement'
    )
    date_paiement = models.DateField()
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2)
    mode_paiement = models.CharField(max_length=50)
    reference = models.CharField(max_length=100)

    def __str__(self):
        return f"Paiement facture {self.facture.id}"

