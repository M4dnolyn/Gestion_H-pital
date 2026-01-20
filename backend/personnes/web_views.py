from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from datetime import date

from .models import Patient, Personnel, ProcheAidant
from .forms import PatientForm, PersonnelForm, ProcheAidantForm

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
    # Imports locaux pour éviter les cycles
    from planning.models import RendezVous
    from medical.models import Consultation
    
    try:
        rendezvous = RendezVous.objects.filter(patient=patient).order_by('-date_rdv')[:5]
    except:
        rendezvous = []
        
    try:
        consultations = Consultation.objects.filter(patient=patient).order_by('-date_consultation')[:5]
    except:
        consultations = []
    
    context = {
        'patient': patient,
        'rendezvous': rendezvous,
        'consultations': consultations,
    }
    return render(request, 'patients/detail.html', context)


@login_required
def patient_create(request):
    """Créer un patient"""
    if request.method == 'POST':
        # Essayer d'abord avec le formulaire complet
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, 'Patient créé avec succès!')
            return redirect('patient_list')
        elif 'nom' in request.POST and 'prenom' in request.POST:
            # Fallback manuel si le form échoue ou n'est pas utilisé
            Patient.objects.create(
                nom=request.POST.get('nom'),
                prenom=request.POST.get('prenom'),
                telephone=request.POST.get('telephone'),
                email=request.POST.get('email')
            )
            messages.success(request, 'Patient créé avec succès!')
            return redirect('patient_list')
    else:
        form = PatientForm()
    
    return render(request, 'patients/form.html', {'form': form})


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


# ==================== VUES PERSONNEL ====================

@login_required
def personnel_list(request):
    """Liste du personnel avec recherche et filtres"""
    personnel_list = Personnel.objects.all().order_by('nom', 'prenom')
    
    # Recherche
    query = request.GET.get('q')
    if query:
        personnel_list = personnel_list.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(email__icontains=query) |
            Q(telephone__icontains=query)
        )
    
    # Filtres
    fonction = request.GET.get('fonction')
    statut = request.GET.get('statut')
    
    if fonction:
        personnel_list = personnel_list.filter(fonction=fonction)
    if statut:
        personnel_list = personnel_list.filter(statut=statut)
    
    # Pagination
    paginator = Paginator(personnel_list, 15)
    page_number = request.GET.get('page')
    personnel = paginator.get_page(page_number)
    
    # Statistiques
    context = {
        'personnel': personnel,
        'total_personnel': Personnel.objects.count(),
        'medecins': Personnel.objects.filter(fonction='MED').count(),
        'infirmiers': Personnel.objects.filter(fonction='INF').count(),
        'personnel_actif': Personnel.objects.filter(statut='ACT').count(),
        'fonctions': Personnel.FONCTIONS,
        'statuts': Personnel.STATUTS,
    }
    return render(request, 'personnes/personnel_list.html', context)


@login_required
def personnel_detail(request, pk):
    """Détail d'un membre du personnel"""
    personnel = get_object_or_404(Personnel, pk=pk)
    
    # Récupérer les services affectés
    try:
        from rh.models import PersonnelService
        services = PersonnelService.objects.filter(personnel=personnel).select_related('service')
    except:
        services = []
        
    # Récupérer les congés
    try:
        from rh.models import Conge
        conges = Conge.objects.filter(personnel=personnel).order_by('-date_debut')[:5]
    except:
        conges = []
    
    # Récupérer les rendez-vous si c'est un médecin
    rendezvous = None
    if personnel.fonction == 'MED':
        try:
            from planning.models import RendezVous
            rendezvous = RendezVous.objects.filter(medecin=personnel).order_by('-date_rdv')[:5]
        except:
            rendezvous = []
    
    context = {
        'personnel': personnel,
        'services': services,
        'conges': conges,
        'rendezvous': rendezvous,
    }
    return render(request, 'personnes/personnel_detail.html', context)


@login_required
def personnel_create(request):
    """Créer un nouveau membre du personnel"""
    if request.method == 'POST':
        form = PersonnelForm(request.POST)
        if form.is_valid():
            personnel = form.save()
            messages.success(request, f'Personnel {personnel.nom_complet} créé avec succès!')
            return redirect('personnel_detail', pk=personnel.pk)
    else:
        form = PersonnelForm()
    
    return render(request, 'personnes/personnel_form.html', {'form': form})


@login_required
def personnel_update(request, pk):
    """Modifier un membre du personnel"""
    personnel = get_object_or_404(Personnel, pk=pk)
    
    if request.method == 'POST':
        form = PersonnelForm(request.POST, instance=personnel)
        if form.is_valid():
            form.save()
            messages.success(request, f'Personnel {personnel.nom_complet} modifié avec succès!')
            return redirect('personnel_detail', pk=personnel.pk)
    else:
        form = PersonnelForm(instance=personnel)
    
    return render(request, 'personnes/personnel_form.html', {
        'form': form,
        'personnel': personnel
    })


@login_required
def personnel_delete(request, pk):
    """Supprimer un membre du personnel"""
    personnel = get_object_or_404(Personnel, pk=pk)
    
    if request.method == 'POST':
        nom = personnel.nom_complet
        personnel.delete()
        messages.success(request, f'Personnel {nom} supprimé avec succès!')
        return redirect('personnel_list')
    
    return render(request, 'personnes/personnel_delete.html', {'personnel': personnel})


# ==================== VUES PROCHE AIDANT ====================

@login_required
def proche_list(request):
    """Liste des proches aidants"""
    proches_list = ProcheAidant.objects.all().order_by('nom', 'prenom')
    
    # Recherche
    query = request.GET.get('q')
    if query:
        proches_list = proches_list.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(telephone__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(proches_list, 15)
    page_number = request.GET.get('page')
    proches = paginator.get_page(page_number)
    
    context = {
        'proches': proches,
        'total_proches': ProcheAidant.objects.count(),
    }
    return render(request, 'personnes/proche_list.html', context)


@login_required
def proche_detail(request, pk):
    """Détail d'un proche aidant"""
    proche = get_object_or_404(ProcheAidant, pk=pk)
    patients = proche.patients.all()
    
    context = {
        'proche': proche,
        'patients': patients,
    }
    return render(request, 'personnes/proche_detail.html', context)


@login_required
def proche_create(request):
    """Créer un nouveau proche aidant"""
    if request.method == 'POST':
        form = ProcheAidantForm(request.POST)
        if form.is_valid():
            proche = form.save()
            messages.success(request, f'Proche aidant {proche.prenom} {proche.nom} créé avec succès!')
            return redirect('proche_detail', pk=proche.pk)
    else:
        form = ProcheAidantForm()
    
    return render(request, 'personnes/proche_form.html', {'form': form})


@login_required
def proche_update(request, pk):
    """Modifier un proche aidant"""
    proche = get_object_or_404(ProcheAidant, pk=pk)
    
    if request.method == 'POST':
        form = ProcheAidantForm(request.POST, instance=proche)
        if form.is_valid():
            form.save()
            messages.success(request, f'Proche aidant {proche.prenom} {proche.nom} modifié avec succès!')
            return redirect('proche_detail', pk=proche.pk)
    else:
        form = ProcheAidantForm(instance=proche)
    
    return render(request, 'personnes/proche_form.html', {
        'form': form,
        'proche': proche
    })


@login_required
def proche_delete(request, pk):
    """Supprimer un proche aidant"""
    proche = get_object_or_404(ProcheAidant, pk=pk)
    
    if request.method == 'POST':
        nom = f"{proche.prenom} {proche.nom}"
        proche.delete()
        messages.success(request, f'Proche aidant {nom} supprimé avec succès!')
        return redirect('proche_list')
    
    return render(request, 'personnes/proche_delete.html', {'proche': proche})
