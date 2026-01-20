from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from personnes.models import Personnel
from .models import Conge
import datetime

User = get_user_model()

class RHTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='staff', password='password')
        self.personnel = Personnel.objects.create(
            user=self.user,
            nom="Worker",
            prenom="Hard",
            date_naissance="1995-05-05",
            telephone="444444444",
            adresse="Office",
            date_embauche="2020-01-01",
            fonction="INF"
        )
        self.client.force_login(self.user)

    def test_conge_creation(self):
        conge = Conge.objects.create(
            personnel=self.personnel,
            date_debut=datetime.date.today(),
            date_fin=datetime.date.today() + datetime.timedelta(days=5),
            motif="Vacances",
            statut="En attente"
        )
        self.assertEqual(conge.duree, 6)  # inclusive days logic if applicable, or just check creation
        self.assertEqual(conge.statut, "En attente")

    def test_conge_list_view(self):
        response = self.client.get(reverse('rh:conge_list'))
        self.assertEqual(response.status_code, 200)
