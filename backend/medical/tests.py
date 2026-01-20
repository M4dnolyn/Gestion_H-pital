from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from personnes.models import Patient, Personnel
from .models import Consultation, Ordonnance
import datetime

User = get_user_model()

class MedicalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='doc', password='password')
        self.medecin = Personnel.objects.create(
            user=self.user,
            nom="House",
            prenom="Gregory",
            date_naissance="1960-05-15",
            telephone="111111111",
            adresse="Hospital",
            date_embauche="2020-01-01",
            fonction="MED"
        )
        self.client.force_login(self.user)
        
        self.patient = Patient.objects.create(
            nom="Cuddy",
            prenom="Lisa",
            date_naissance="1970-01-01",
            telephone="222222222",
            adresse="Hospital Admin",
            groupe_sanguin="A+"
        )

    def test_consultation_creation(self):
        """Test creating a consultation via model"""
        cons = Consultation.objects.create(
            patient=self.patient,
            medecin=self.medecin,
            date_consultation=datetime.date.today(),
            heure_consultation=datetime.time(10, 0),
            diagnostic="Lupus",
            observations_cliniques="Never Lupus"
        )
        self.assertEqual(Consultation.objects.count(), 1)
        self.assertEqual(cons.diagnostic, "Lupus")

    def test_consultation_view_access(self):
        """Test accessing consultation list"""
        response = self.client.get(reverse('consultation_list'))
        self.assertEqual(response.status_code, 200)

    def test_ordonnance_creation(self):
        """Test creating an ordonnance linked to consultation"""
        cons = Consultation.objects.create(
            patient=self.patient,
            medecin=self.medecin,
            date_consultation=datetime.date.today(),
            heure_consultation=datetime.time(14, 0),
            diagnostic="Flu"
        )
        ordonnance = Ordonnance.objects.create(
            consultation=cons,
            contenu_medical="Paracetamol 1000mg"
        )
        self.assertEqual(Ordonnance.objects.count(), 1)
        self.assertEqual(ordonnance.consultation, cons)
