
import os
import django
import random
from datetime import date, timedelta, time

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from personnes.models import Patient, Personnel
from services.models import Service
from planning.models import RendezVous
from medical.models import Consultation, Ordonnance
from billing.models import Facture, Prestation

User = get_user_model()

def populate():
    print("Deleting old data...")
    RendezVous.objects.all().delete()
    Consultation.objects.all().delete()
    Patient.objects.all().delete()
    Personnel.objects.all().delete()
    Service.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()
    
    print("Creating Services...")
    services_list = ['Cardiologie', 'Pédiatrie', 'Urgence', 'Radiologie', 'Chirurgie']
    services = []
    for s_name in services_list:
        service = Service.objects.create(nom_service=s_name, description=f"Service de {s_name}", localisation="Batiment A")
        services.append(service)

    print("Creating Personnel...")
    medecins = []
    # Create Medecin
    for i in range(5):
        user = User.objects.create_user(username=f'medecin{i}', password='password123', email=f'med{i}@hopital.com')
        doc = Personnel.objects.create(
            user=user,
            nom=f"Medecin{i}", prenom=f"Doc{i}",
            date_naissance="1980-01-01", telephone=f"06000000{i}",
            adresse="1 rue Medicale", fonction='MED',
            date_embauche="2020-01-01"
        )
        medecins.append(doc)
    
    # Create Staff logic if needed (Nurse, Admin)
    
    print("Creating Patients...")
    patients = []
    for i in range(10):
        pat = Patient.objects.create(
            nom=f"Patient{i}", prenom=f"Test{i}",
            date_naissance="1990-05-20", telephone=f"07000000{i}",
            adresse="10 rue des Patients", groupe_sanguin=random.choice(['A+', 'O+', 'B-']),
            assurance=f"Assurance-{i}"
        )
        patients.append(pat)

    print("Creating RendezVous...")
    for i in range(10):
        RendezVous.objects.create(
            patient=random.choice(patients),
            medecin=random.choice(medecins),
            date_rdv=date.today() + timedelta(days=random.randint(-2, 5)),
            heure_rdv=time(9 + i, 0),
            motif="Consultation de routine",
            statut_rdv="Programmé"
        )

    print("Creating Consultations and Ordonnances...")
    for i in range(5):
        cons = Consultation.objects.create(
            patient=patients[i],
            medecin=medecins[i % len(medecins)],
            date_consultation=date.today(),
            heure_consultation=time(14, 30),
            diagnostic="Reflux gastrique simple",
            observations_cliniques="Patient se plaint de bruleurs d'estomac"
        )
        Ordonnance.objects.create(
            consultation=cons,
            contenu_medical="Gaviscon 3x/jour après repas"
        )

    print("Database populated successfully!")

if __name__ == '__main__':
    populate()
