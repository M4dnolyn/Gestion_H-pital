# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date, datetime, timedelta
import json

# Importez vos modèles ici
from .models import Patient, RendezVous, Consultation, Medecin
from .forms import PatientForm, RendezVousForm, ConsultationForm

# ==================== VUES PUBLIQUES ====================

def index(request):
    """Page d'accueil publique"""
    return render(request, 'index.html')


# ==================== DASHBOARD ====================

@login_required
def dashboard(request):
    """Tableau de bord après connexion"""
    today = date.today()
    
    context = {
        'total_patients': Patient.objects.count(),
        'total_personnel': 156,  # À remplacer par ton modèle
        'consultations_aujourdhui': Consultation.objects.filter(date=today).count(),
        'rdv_en_attente': RendezVous.objects.filter(statut='en attente').count(),
        'patients_recents': Patient.objects.order_by('-date_creation')[:3],
        'prochains_rdv': RendezVous.objects.filter(date__gte=today).order_by('date', 'heure_debut')[:5],  # CORRIGÉ
        'paiements_du_jour': 45,  # AJOUTER
    }
    return render(request, 'dashboard/index.html', context)
# Dans config/views.py, ajoute cette vue après dashboard()
@login_required
def dashboard_roles(request):
    """Tableau de bord pour la gestion des rôles"""
    today = date.today()
    
    context = {
        'total_patients': Patient.objects.count(),
        'total_personnel': 156,
        'consultations_aujourdhui': Consultation.objects.filter(date=today).count(),
        'rdv_en_attente': RendezVous.objects.filter(statut='en attente').count(),
        'patients_recents': Patient.objects.order_by('-date_creation')[:3],
        'prochains_rdv': RendezVous.objects.filter(date__gte=today).order_by('date', 'heure_debut')[:5],
        'paiements_du_jour': 45,
    }
    return render(request, 'dashboard/roles/index.html', context)
# ==================== VUES PATIENTS ====================

@login_required
def patient_list(request):
    """Liste des patients avec recherche et pagination"""
    patients_list = Patient.objects.all().order_by('-id')
    
    # Recherche
    query = request.GET.get('q')
    if query:
        patients_list = patients_list.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(telephone__icontains=query) |
            Q(email__icontains=query)
        )
    
    # Pagination (10 patients par page)
    paginator = Paginator(patients_list, 10)
    page_number = request.GET.get('page')
    patients = paginator.get_page(page_number)
    
    return render(request, 'patients/list.html', {'patients': patients})


@login_required
def patient_detail(request, pk):
    """Détail d'un patient"""
    patient = get_object_or_404(Patient, pk=pk)
    
    # Récupérer les rendez-vous et consultations du patient
    rendezvous = RendezVous.objects.filter(patient=patient).order_by('-date')[:5]
    consultations = Consultation.objects.filter(patient=patient).order_by('-date')[:5]
    
    context = {
        'patient': patient,
        'rendezvous': rendezvous,
        'consultations': consultations,
    }
    return render(request, 'patients/detail.html', context)


# Dans config/views.py - AJOUTE si elles n'existent pas

@login_required
def patient_create(request):
    """Créer un patient (version simplifiée)"""
    if request.method == 'POST':
        # Version simple sans formulaire
        Patient.objects.create(
            nom=request.POST.get('nom'),
            prenom=request.POST.get('prenom'),
            telephone=request.POST.get('telephone'),
            email=request.POST.get('email')
        )
        messages.success(request, 'Patient créé avec succès!')
        return redirect('patient_list')
    
    return render(request, 'patients/form.html')

@login_required
def patient_detail(request, pk):
    """Détail d'un patient"""
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patients/detail.html', {'patient': patient})

@login_required
def patient_update(request, pk):
    """Modifier un patient existant"""
    patient = get_object_or_404(Patient, pk=pk)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f'Patient {patient.nom} {patient.prenom} modifié avec succès!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    
    return render(request, 'patients/form.html', {'form': form, 'patient': patient})


@login_required
def patient_delete(request, pk):
    """Supprimer un patient"""
    patient = get_object_or_404(Patient, pk=pk)
    
    if request.method == 'POST':
        patient.delete()
        messages.success(request, f'Patient {patient.nom} {patient.prenom} supprimé avec succès!')
        return redirect('patient_list')
    
    return render(request, 'patients/delete.html', {'patient': patient})


# ==================== VUES RENDEZ-VOUS ====================

@login_required
def rendezvous_list(request):
    """Liste des rendez-vous avec vue calendrier/liste"""
    view_type = request.GET.get('view', 'list')
    status = request.GET.get('status')
    
    rendezvous_list = RendezVous.objects.all().order_by('-date', '-heure_debut')
    
    # Filtres par statut
    today = date.today()
    if status == 'today':
        rendezvous_list = rendezvous_list.filter(date=today)
    elif status == 'upcoming':
        rendezvous_list = rendezvous_list.filter(date__gte=today)
    elif status == 'past':
        rendezvous_list = rendezvous_list.filter(date__lt=today)
    
    # Pagination pour la vue liste
    if view_type == 'list':
        paginator = Paginator(rendezvous_list, 15)
        page_number = request.GET.get('page')
        rendezvous = paginator.get_page(page_number)
    else:
        rendezvous = rendezvous_list
    
    medecins = Medecin.objects.all()
    
    context = {
        'rendezvous_list': rendezvous,
        'view_type': view_type,
        'medecins': medecins,
    }
    return render(request, 'rendezvous/list.html', context)


@login_required
def rendezvous_detail(request, pk):
    """Détail d'un rendez-vous"""
    rdv = get_object_or_404(RendezVous, pk=pk)
    return render(request, 'rendezvous/detail.html', {'rdv': rdv})


@login_required
def rendezvous_create(request):
    """Créer un rendez-vous (version simplifiée)"""
    if request.method == 'POST':
        try:
            patient = Patient.objects.get(id=request.POST.get('patient'))
            RendezVous.objects.create(
                patient=patient,
                date=request.POST.get('date'),
                heure_debut=request.POST.get('heure_debut'),
                heure_fin=request.POST.get('heure_fin'),
                type=request.POST.get('type', 'consultation'),
                statut='en attente'
            )
            messages.success(request, 'Rendez-vous programmé avec succès!')
            return redirect('rendezvous_list')
        except Patient.DoesNotExist:
            messages.error(request, 'Patient non trouvé')
    
    patients = Patient.objects.all()
    return render(request, 'rendezvous/form.html', {'patients': patients})



@login_required
def rendezvous_update(request, pk):
    """Modifier un rendez-vous existant"""
    rdv = get_object_or_404(RendezVous, pk=pk)
    
    if request.method == 'POST':
        form = RendezVousForm(request.POST, instance=rdv)
        if form.is_valid():
            form.save()
            messages.success(request, f'Rendez-vous modifié avec succès!')
            return redirect('rendezvous_detail', pk=rdv.pk)
    else:
        form = RendezVousForm(instance=rdv)
    
    return render(request, 'rendezvous/form.html', {'form': form, 'rdv': rdv})


@login_required
def rendezvous_delete(request, pk):
    """Supprimer un rendez-vous"""
    rdv = get_object_or_404(RendezVous, pk=pk)
    
    if request.method == 'POST':
        rdv.delete()
        messages.success(request, 'Rendez-vous supprimé avec succès!')
        return redirect('rendezvous_list')
    
    return render(request, 'rendezvous/delete.html', {'rdv': rdv})


@login_required
def rendezvous_cancel(request, pk):
    """Annuler un rendez-vous (changer son statut)"""
    rdv = get_object_or_404(RendezVous, pk=pk)
    
    if request.method == 'POST':
        rdv.statut = 'annulé'
        rdv.save()
        messages.warning(request, 'Rendez-vous annulé!')
        return redirect('rendezvous_detail', pk=rdv.pk)
    
    return render(request, 'rendezvous/cancel.html', {'rdv': rdv})


@login_required
def rendezvous_calendar_api(request):
    """API pour le calendrier des rendez-vous (format JSON)"""
    start = request.GET.get('start', date.today().isoformat())
    end = request.GET.get('end', (date.today() + timedelta(days=30)).isoformat())
    
    rendezvous = RendezVous.objects.filter(
        date__gte=start,
        date__lte=end
    ).select_related('patient', 'medecin')
    
    events = []
    for rdv in rendezvous:
        # Définir la couleur selon le statut
        if rdv.statut == 'confirmé':
            color = '#28a745'  # Vert
        elif rdv.statut == 'annulé':
            color = '#dc3545'  # Rouge
        elif rdv.statut == 'reporté':
            color = '#ffc107'  # Jaune
        else:
            color = '#6c757d'  # Gris
        
        events.append({
            'id': rdv.id,
            'title': f"{rdv.patient.nom} {rdv.prenom} - {rdv.type}",
            'start': f"{rdv.date.isoformat()}T{rdv.heure_debut}",
            'end': f"{rdv.date.isoformat()}T{rdv.heure_fin}",
            'color': color,
            'extendedProps': {
                'patient': str(rdv.patient),
                'medecin': str(rdv.medecin) if rdv.medecin else '',
                'statut': rdv.statut,
                'notes': rdv.notes or ''
            }
        })
    
    return JsonResponse(events, safe=False)


# ==================== VUES CONSULTATIONS ====================

@login_required
def consultation_list(request):
    """Liste des consultations avec filtres"""
    consultations = Consultation.objects.all().order_by('-date', '-heure')
    
    # Filtres
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    medecin_id = request.GET.get('medecin')
    
    if date_debut:
        consultations = consultations.filter(date__gte=date_debut)
    if date_fin:
        consultations = consultations.filter(date__lte=date_fin)
    if medecin_id:
        consultations = consultations.filter(medecin_id=medecin_id)
    
    # Statistiques
    today = date.today()
    month_start = date(today.year, today.month, 1)
    
    context = {
        'consultations': consultations,
        'medecins': Medecin.objects.all(),
        'consultations_ce_mois': Consultation.objects.filter(date__gte=month_start).count(),
        'consultations_aujourdhui': Consultation.objects.filter(date=today).count(),
        'avec_ordonnance': Consultation.objects.filter(ordonnance_requise=True).count(),
    }
    return render(request, 'consultations/list.html', context)


@login_required
def consultation_detail(request, pk):
    """Détail d'une consultation"""
    consultation = get_object_or_404(Consultation, pk=pk)
    return render(request, 'consultations/detail.html', {'consultation': consultation})


@login_required
def consultation_create(request):
    """Créer une consultation (version simplifiée)"""
    if request.method == 'POST':
        try:
            patient = Patient.objects.get(id=request.POST.get('patient'))
            Consultation.objects.create(
                patient=patient,
                date=request.POST.get('date'),
                heure=request.POST.get('heure'),
                motif=request.POST.get('motif'),
                diagnostic=request.POST.get('diagnostic', ''),
                statut='terminée'
            )
            messages.success(request, 'Consultation enregistrée avec succès!')
            return redirect('consultation_list')
        except Patient.DoesNotExist:
            messages.error(request, 'Patient non trouvé')
    
    patients = Patient.objects.all()
    return render(request, 'consultations/form.html', {'patients': patients})

@login_required
def consultation_update(request, pk):
    """Modifier une consultation existante"""
    consultation = get_object_or_404(Consultation, pk=pk)
    
    if request.method == 'POST':
        form = ConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            form.save()
            messages.success(request, f'Consultation modifiée avec succès!')
            return redirect('consultation_detail', pk=consultation.pk)
    else:
        form = ConsultationForm(instance=consultation)
    
    return render(request, 'consultations/form.html', {'form': form, 'consultation': consultation})


@login_required
def consultation_delete(request, pk):
    """Supprimer une consultation"""
    consultation = get_object_or_404(Consultation, pk=pk)
    
    if request.method == 'POST':
        consultation.delete()
        messages.success(request, 'Consultation supprimée avec succès!')
        return redirect('consultation_list')
    
    return render(request, 'consultations/delete.html', {'consultation': consultation})
