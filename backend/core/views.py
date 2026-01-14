# core/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date

# ------------------------------------------------------------
# FONCTIONS DE VÉRIFICATION DES RÔLES (CORRIGÉES)
# ------------------------------------------------------------

def get_personnel(user):
    """Récupère le profil Personnel de l'utilisateur"""
    try:
        # CORRECTION : utiliser personnel_profile au lieu de personnel
        if hasattr(user, 'personnel_profile'):
            return user.personnel_profile
    except:
        pass
    return None

def is_medecin(user):
    """Vérifie si l'utilisateur est un médecin"""
    personnel = get_personnel(user)
    return personnel is not None and personnel.fonction == 'MED'

def is_infirmier(user):
    """Vérifie si l'utilisateur est un infirmier"""
    personnel = get_personnel(user)
    return personnel is not None and personnel.fonction == 'INF'

def is_agent_admin(user):
    """Vérifie si l'utilisateur est un agent administratif"""
    personnel = get_personnel(user)
    return personnel is not None and personnel.fonction == 'ADM'

def is_caissier(user):
    """Vérifie si l'utilisateur est un caissier"""
    personnel = get_personnel(user)
    return personnel is not None and personnel.fonction == 'CAI'

def is_responsable(user):
    """Vérifie si l'utilisateur est un responsable de service"""
    personnel = get_personnel(user)
    return personnel is not None and personnel.fonction == 'RES'

def is_direction(user):
    """Vérifie si l'utilisateur est de la direction"""
    personnel = get_personnel(user)
    return personnel is not None and personnel.fonction == 'DIR'

# ------------------------------------------------------------
# VUE PRINCIPALE DASHBOARD (CORRIGÉE)
# ------------------------------------------------------------

@login_required
def dashboard(request):
    """
    Tableau de bord principal adapté au rôle de l'utilisateur.
    """
    today = date.today()
    user = request.user
    
    # Contexte de base pour tous les utilisateurs
    context = {
        'user': user,
        'today': today,
    }
    
    # Récupérer le profil Personnel si existe
    personnel = get_personnel(user)
    
    if personnel is not None:
        context['personnel'] = personnel
        context['role'] = personnel.fonction
        context['role_display'] = personnel.get_fonction_display()
        
        # Données spécifiques selon le rôle
        fonction = personnel.fonction
        
        if fonction == 'MED':  # MÉDECIN
            context.update({
                'title': 'Dashboard Médecin',
                'icon': 'fa-user-md',
            })
            
        elif fonction == 'INF':  # INFIRMIER
            context.update({
                'title': 'Dashboard Infirmier',
                'icon': 'fa-user-nurse',
            })
            
        elif fonction == 'ADM':  # AGENT ADMINISTRATIF
            context.update({
                'title': 'Dashboard Administratif',
                'icon': 'fa-user-tie',
            })
            
        elif fonction == 'CAI':  # CAISSIER
            context.update({
                'title': 'Dashboard Caissier',
                'icon': 'fa-cash-register',
            })
            
        elif fonction == 'RES':  # RESPONSABLE DE SERVICE
            context.update({
                'title': 'Dashboard Responsable',
                'icon': 'fa-chart-line',
            })
                
        elif fonction == 'DIR':  # DIRECTION
            context.update({
                'title': 'Dashboard Direction',
                'icon': 'fa-chart-bar',
            })
            
        elif fonction == 'ADMIN':  # ADMIN SYSTÈME
            context.update({
                'title': 'Dashboard Administrateur',
                'icon': 'fa-cogs',
            })
    
    else:
        # Utilisateur sans profil personnel (superadmin)
        context.update({
            'title': 'Dashboard Administrateur',
            'icon': 'fa-cogs',
            'is_superuser': user.is_superuser,
        })
    
    # Charger les données dynamiques AVEC GESTION D'ERREUR
    try:
        from personnes.models import Patient, Personnel as PersModel
        from planning.models import RendezVous
        from medical.models import Consultation
        from billing.models import Facture, FacturePrestation
        from rh.models import Conge
        from services.models import Service
        
        # Données communes
        context.update({
            'patient_count': Patient.objects.count(),
            'personnel_count': PersModel.objects.count(),
            'services': Service.objects.all()[:4],
            'recent_patients': Patient.objects.order_by('-date_inscription')[:5],
            'consultations_today': Consultation.objects.filter(date_consultation=today).count(),
            'conges_en_attente': Conge.objects.filter(statut_conge='En attente').count(),
        })
        
        # Données conditionnelles par rôle
        if personnel is not None:
            if personnel.fonction == 'MED':
                try:
                    context.update({
                        'mes_rdv_aujourdhui': RendezVous.objects.filter(
                            medecin=personnel,
                            date_rdv=today
                        ).count(),
                        'mes_consultations': Consultation.objects.filter(
                            medecin=personnel,
                            date_consultation=today
                        ).count(),
                    })
                except:
                    context.update({
                        'mes_rdv_aujourdhui': 0,
                        'mes_consultations': 0,
                    })
                    
            elif personnel.fonction == 'CAI':
                try:
                    factures_payees = Facture.objects.filter(
                        date_facture=today,
                        statut_paiement='Soldée'
                    )
                    montant_total = 0
                    for f in factures_payees:
                        for ligne in FacturePrestation.objects.filter(facture=f):
                            montant_total += ligne.montant_ligne()
                    
                    context.update({
                        'paiements_today': factures_payees.count(),
                        'montant_today': montant_total,
                    })
                except:
                    context.update({
                        'paiements_today': 0,
                        'montant_today': 0,
                    })
        
        # Rendez-vous à venir (pour tous)
        try:
            upcoming = RendezVous.objects.filter(
                date_rdv__gte=today
            ).order_by('date_rdv', 'heure_rdv')[:5]
            context['upcoming_rdv'] = upcoming
        except:
            context['upcoming_rdv'] = []
            
    except ImportError as e:
        # Si un modèle n'existe pas
        context['error'] = f"Modèle manquant: {e}"
        context.update({
            'patient_count': 0,
            'personnel_count': 0,
            'services': [],
            'recent_patients': [],
            'consultations_today': 0,
            'conges_en_attente': 0,
            'upcoming_rdv': [],
        })
    except Exception as e:
        # Erreur générale
        context['error'] = f"Erreur chargement données: {e}"
        context.update({
            'patient_count': 0,
            'personnel_count': 0,
            'services': [],
            'recent_patients': [],
            'consultations_today': 0,
            'conges_en_attente': 0,
            'upcoming_rdv': [],
        })
    
    # Déterminer le template à utiliser
    template_name = 'dashboard/index.html'
    if 'role' in context:
        role = context['role']
        # Si vous avez des templates spécifiques par rôle
        if role in ['MED', 'INF', 'ADM', 'CAI']:
            template_name = f'dashboard/roles/{role.lower()}.html'
    
    return render(request, template_name, context)

# ------------------------------------------------------------
# VUES SPÉCIFIQUES PAR RÔLE (MAINTENANT INUTILES SI VOUS AVEZ DÉJÀ LES TEMPLATES)
# ------------------------------------------------------------

@login_required
@user_passes_test(is_medecin)
def dashboard_medecin(request):
    """Dashboard spécifique pour les médecins seulement"""
    today = date.today()
    personnel = get_personnel(request.user)
    
    context = {
        'personnel': personnel,
        'title': 'Espace Médecin',
    }
    
    try:
        from planning.models import RendezVous
        from personnes.models import Patient
        
        context.update({
            'mes_rdv': RendezVous.objects.filter(medecin=personnel, date_rdv=today),
            'mes_patients': Patient.objects.filter(
                consultations__medecin=personnel
            ).distinct(),
        })
    except:
        context.update({
            'mes_rdv': [],
            'mes_patients': [],
        })
    
    return render(request, 'dashboard/roles/medecin.html', context)

@login_required
@user_passes_test(is_infirmier)
def dashboard_infirmier(request):
    """Dashboard spécifique pour les infirmiers seulement"""
    context = {
        'title': 'Espace Infirmier',
        'personnel': get_personnel(request.user),
    }
    return render(request, 'dashboard/roles/infirmier.html', context)

@login_required
@user_passes_test(is_agent_admin)
def dashboard_admin(request):
    """Dashboard spécifique pour les agents administratifs"""
    today = date.today()
    
    context = {
        'title': 'Espace Administratif',
        'personnel': get_personnel(request.user),
    }
    
    try:
        from planning.models import RendezVous
        from personnes.models import Patient
        
        context.update({
            'rdv_aujourdhui': RendezVous.objects.filter(date_rdv=today),
            'nouveaux_patients': Patient.objects.filter(date_inscription=today),
        })
    except:
        context.update({
            'rdv_aujourdhui': [],
            'nouveaux_patients': [],
        })
    
    return render(request, 'dashboard/roles/admin.html', context)

# ------------------------------------------------------------
# VUES POUR LES AUTRES PAGES
# ------------------------------------------------------------

@login_required
def patients_list(request):
    """Liste des patients"""
    try:
        from personnes.models import Patient
        patients = Patient.objects.all()[:50]
        return render(request, 'patients/list.html', {'patients': patients})
    except:
        return render(request, 'patients/list.html', {'patients': [], 'error': 'Données non disponibles'})

@login_required
def personnel_list(request):
    """Liste du personnel"""
    try:
        from personnes.models import Personnel
        personnel = Personnel.objects.all()[:50]
        return render(request, 'personnel/list.html', {'personnel': personnel})
    except:
        return render(request, 'personnel/list.html', {'personnel': [], 'error': 'Données non disponibles'})

@login_required
def appointments(request):
    """Rendez-vous"""
    try:
        from planning.models import RendezVous
        rdvs = RendezVous.objects.all()[:50]
        return render(request, 'rendezvous/list.html', {'rdvs': rdvs})
    except:
        return render(request, 'rendezvous/list.html', {'rdvs': [], 'error': 'Données non disponibles'})

@login_required
def consultations(request):
    """Consultations"""
    try:
        from medical.models import Consultation
        consultations = Consultation.objects.all()[:50]
        return render(request, 'consultations/list.html', {'consultations': consultations})
    except:
        return render(request, 'consultations/list.html', {'consultations': [], 'error': 'Données non disponibles'})

# ------------------------------------------------------------
# VUES D'AUTHENTIFICATION
# ------------------------------------------------------------

def logout_view(request):
    """Gère la déconnexion GET et POST"""
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'accounts/logout_confirm.html')

def logout_confirm(request):
    """Page de confirmation de déconnexion"""
    return render(request, 'accounts/logout_confirm.html', {
        'user': request.user,
    })

# ------------------------------------------------------------
# VUE DE TEST ET API
# ------------------------------------------------------------

def test_view(request):
    """Vue de test pour vérifier l'installation"""
    return render(request, 'test.html', {
        'message': 'Django fonctionne correctement !',
        'user': request.user,
    })

@api_view(['GET'])
def health_check(request):
    return Response({
        'status': 'ok',
        'service': 'Hospital Management API',
        'version': '1.0'
    })