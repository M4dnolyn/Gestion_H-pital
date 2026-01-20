from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from personnes.models import Patient
from .models import Facture, Prestation

class BillingTests(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            nom="Pay",
            prenom="Master",
            date_naissance="1990-09-09",
            telephone="333333333",
            adresse="Bank St"
        )
        self.user = get_user_model().objects.create_user(username='billing_user', password='password')
        self.client = Client()
        self.client.force_login(self.user)

    def test_prestation_model(self):
        prestation = Prestation.objects.create(
            nom="Consultation Generaliste",
            prix=25.0
        )
        self.assertEqual(prestation.prix, 25.0)

    def test_facture_creation(self):
        facture = Facture.objects.create(
            patient=self.patient,
            statut='Impayée'
        )
        self.assertEqual(facture.statut, 'Impayée')
        self.assertEqual(facture.montant_total, 0)
    
    def test_facture_list_view(self):
        response = self.client.get(reverse('billing:facture_list'))
        self.assertEqual(response.status_code, 200)
