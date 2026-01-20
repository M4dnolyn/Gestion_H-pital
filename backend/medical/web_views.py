from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Ordonnance, Consultation
from .forms import OrdonnanceForm

@login_required
def ordonnance_list(request):
    """Liste des ordonnances"""
    ordonnances_list = Ordonnance.objects.select_related('consultation', 'consultation__patient', 'consultation__medecin').all().order_by('-id')
    
    # Recherche
    query = request.GET.get('q')
    if query:
        ordonnances_list = ordonnances_list.filter(
            Q(consultation__patient__nom__icontains=query) |
            Q(consultation__patient__prenom__icontains=query) |
            Q(contenu_medical__icontains=query)
        )
    
    paginator = Paginator(ordonnances_list, 10)
    page_number = request.GET.get('page')
    ordonnances = paginator.get_page(page_number)
    
    return render(request, 'medical/ordonnance_list.html', {'ordonnances': ordonnances})

@login_required
def ordonnance_create(request):
    """Créer une ordonnance"""
    if request.method == 'POST':
        form = OrdonnanceForm(request.POST)
        if form.is_valid():
            ordonnance = form.save()
            messages.success(request, "Ordonnance créée avec succès.")
            return redirect('ordonnance_detail', pk=ordonnance.pk)
    else:
        # Pré-remplir si consultation_id est fourni
        consultation_id = request.GET.get('consultation')
        initial = {}
        if consultation_id:
            initial['consultation'] = consultation_id
        form = OrdonnanceForm(initial=initial)
    
    return render(request, 'medical/ordonnance_form.html', {'form': form})

@login_required
def ordonnance_detail(request, pk):
    """Détails d'une ordonnance"""
    ordonnance = get_object_or_404(Ordonnance, pk=pk)
    return render(request, 'medical/ordonnance_detail.html', {'ordonnance': ordonnance})

@login_required
def ordonnance_update(request, pk):
    """Modifier une ordonnance"""
    ordonnance = get_object_or_404(Ordonnance, pk=pk)
    if request.method == 'POST':
        form = OrdonnanceForm(request.POST, instance=ordonnance)
        if form.is_valid():
            form.save()
            messages.success(request, "Ordonnance mise à jour avec succès.")
            return redirect('ordonnance_detail', pk=pk)
    else:
        form = OrdonnanceForm(instance=ordonnance)
    
    return render(request, 'medical/ordonnance_form.html', {'form': form, 'ordonnance': ordonnance})

@login_required
def ordonnance_delete(request, pk):
    """Supprimer une ordonnance"""
    ordonnance = get_object_or_404(Ordonnance, pk=pk)
    if request.method == 'POST':
        ordonnance.delete()
        messages.success(request, "Ordonnance supprimée avec succès.")
        return redirect('ordonnance_list')
    
    return render(request, 'medical/ordonnance_delete.html', {'ordonnance': ordonnance})


# ==================== VUES CONSULTATIONS ====================

@login_required
def consultation_list(request):
    """Liste des consultations avec filtres"""
    consultations = Consultation.objects.all().order_by('-date_consultation', '-heure_consultation')
    
    # Filtres
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    medecin_id = request.GET.get('medecin')
    
    if date_debut:
        consultations = consultations.filter(date_consultation__gte=date_debut)
    if date_fin:
        consultations = consultations.filter(date_consultation__lte=date_fin)
    if medecin_id:
        consultations = consultations.filter(medecin_id=medecin_id)
    
    # Statistiques contextuelles (optionnel, pour éviter les erreurs si modèles non importés)
    from datetime import date
    today = date.today()
    month_start = date(today.year, today.month, 1)
    
    # Import local pour éviter cycle avec Personnel (via medecin_id)
    from personnes.models import Personnel
    
    context = {
        'consultations': consultations,
        'medecins': Personnel.objects.filter(fonction='MED'),
        'consultations_ce_mois': Consultation.objects.filter(date_consultation__gte=month_start).count(),
        'consultations_aujourdhui': Consultation.objects.filter(date_consultation=today).count(),
        'avec_ordonnance': Consultation.objects.filter(ordonnance__isnull=False).count(),
    }
    return render(request, 'consultations/list.html', context)


@login_required
def consultation_detail(request, pk):
    """Détail d'une consultation"""
    consultation = get_object_or_404(Consultation, pk=pk)
    return render(request, 'consultations/detail.html', {'consultation': consultation})


@login_required
def consultation_create(request):
    """Créer une consultation"""
    # Import local du formulaire pour éviter circularité si le form import medical.views (peu probable mais prudent)
    from .forms import ConsultationForm 
    
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save()
            messages.success(request, 'Consultation enregistrée avec succès!')
            return redirect('consultation_detail', pk=consultation.pk)
    else:
        # Pré-remplir si patient_id est fourni
        patient_id = request.GET.get('patient')
        initial = {}
        if patient_id:
            initial['patient'] = patient_id
        form = ConsultationForm(initial=initial)
    
    return render(request, 'consultations/form.html', {'form': form})

@login_required
def consultation_update(request, pk):
    """Modifier une consultation existante"""
    consultation = get_object_or_404(Consultation, pk=pk)
    from .forms import ConsultationForm
    
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
