from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.decorators import role_required
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date

from .models import Conge, PersonnelService
from .forms import CongeForm, PersonnelServiceForm
from personnes.models import Personnel
from services.models import Service


# ==================== VUES CONGÉS ====================

@login_required
def conge_list(request):
    """Liste des congés avec filtres"""
    conges_list = Conge.objects.all().order_by('-date_debut')
    
    # Filtres
    statut = request.GET.get('statut')
    type_conge = request.GET.get('type')
    personnel_id = request.GET.get('personnel')
    
    if statut:
        conges_list = conges_list.filter(statut_conge=statut)
    if type_conge:
        conges_list = conges_list.filter(type_conge=type_conge)
    if personnel_id:
        conges_list = conges_list.filter(personnel_id=personnel_id)
    
    # Pagination
    paginator = Paginator(conges_list, 15)
    page_number = request.GET.get('page')
    conges = paginator.get_page(page_number)
    
    # Statistiques
    today = date.today()
    context = {
        'conges': conges,
        'personnel_list': Personnel.objects.all(),
        'total_conges': Conge.objects.count(),
        'conges_en_attente': Conge.objects.filter(statut_conge='En attente').count(),
        'conges_approuves': Conge.objects.filter(statut_conge='Approuvé').count(),
        'conges_en_cours': Conge.objects.filter(
            date_debut__lte=today,
            date_fin__gte=today,
            statut_conge='Approuvé'
        ).count(),
    }
    return render(request, 'rh/conge_list.html', context)


@login_required
def conge_detail(request, pk):
    """Détail d'un congé"""
    conge = get_object_or_404(Conge, pk=pk)
    
    # Calculer la durée
    duree = (conge.date_fin - conge.date_debut).days + 1
    
    context = {
        'conge': conge,
        'duree': duree,
    }
    return render(request, 'rh/conge_detail.html', context)


@login_required
def conge_create(request):
    """Créer une demande de congé"""
    if request.method == 'POST':
        form = CongeForm(request.POST)
        if form.is_valid():
            conge = form.save()
            messages.success(request, 'Demande de congé créée avec succès!')
            return redirect('rh:conge_detail', pk=conge.pk)
    else:
        form = CongeForm()
    
    return render(request, 'rh/conge_form.html', {'form': form})


@login_required
def conge_update(request, pk):
    """Modifier une demande de congé"""
    conge = get_object_or_404(Conge, pk=pk)
    
    if request.method == 'POST':
        form = CongeForm(request.POST, instance=conge)
        if form.is_valid():
            form.save()
            messages.success(request, 'Demande de congé modifiée avec succès!')
            return redirect('rh:conge_detail', pk=conge.pk)
    else:
        form = CongeForm(instance=conge)
    
    return render(request, 'rh/conge_form.html', {
        'form': form,
        'conge': conge
    })


@login_required
def conge_delete(request, pk):
    """Supprimer une demande de congé"""
    conge = get_object_or_404(Conge, pk=pk)
    
    if request.method == 'POST':
        conge.delete()
        messages.success(request, 'Demande de congé supprimée avec succès!')
        return redirect('rh:conge_list')
    
    return render(request, 'rh/conge_delete.html', {'conge': conge})


@login_required
@role_required(['ADMIN', 'DIR', 'RES'])
def conge_approve(request, pk):
    """Approuver une demande de congé"""
    conge = get_object_or_404(Conge, pk=pk)
    
    if request.method == 'POST':
        conge.statut_conge = 'Approuvé'
        conge.save()
        messages.success(request, f'Congé de {conge.personnel} approuvé!')
        return redirect('rh:conge_detail', pk=conge.pk)
    
    return render(request, 'rh/conge_approve.html', {'conge': conge})


@login_required
def conge_reject(request, pk):
    """Refuser une demande de congé"""
    conge = get_object_or_404(Conge, pk=pk)
    
    if request.method == 'POST':
        conge.statut_conge = 'Refusé'
        conge.save()
        messages.warning(request, f'Congé de {conge.personnel} refusé!')
        return redirect('rh:conge_detail', pk=conge.pk)
    
    return render(request, 'rh/conge_reject.html', {'conge': conge})


# ==================== VUES PERSONNEL-SERVICE ====================

@login_required
def personnel_service_list(request):
    """Liste des affectations personnel-service"""
    affectations_list = PersonnelService.objects.all().order_by('-date_affectation')
    
    # Filtres
    service_id = request.GET.get('service')
    personnel_id = request.GET.get('personnel')
    
    if service_id:
        affectations_list = affectations_list.filter(service_id=service_id)
    if personnel_id:
        affectations_list = affectations_list.filter(personnel_id=personnel_id)
    
    # Pagination
    paginator = Paginator(affectations_list, 20)
    page_number = request.GET.get('page')
    affectations = paginator.get_page(page_number)
    
    context = {
        'affectations': affectations,
        'services': Service.objects.all(),
        'personnel_list': Personnel.objects.all(),
    }
    return render(request, 'rh/personnel_service_list.html', context)


@login_required
def personnel_service_create(request):
    """Affecter un personnel à un service"""
    if request.method == 'POST':
        form = PersonnelServiceForm(request.POST)
        if form.is_valid():
            affectation = form.save()
            messages.success(request, f'{affectation.personnel} affecté(e) au service {affectation.service}!')
            return redirect('rh:personnel_service_list')
    else:
        form = PersonnelServiceForm()
    
    return render(request, 'rh/personnel_service_form.html', {'form': form})


@login_required
def personnel_service_delete(request, pk):
    """Supprimer une affectation"""
    affectation = get_object_or_404(PersonnelService, pk=pk)
    
    if request.method == 'POST':
        personnel = affectation.personnel
        service = affectation.service
        affectation.delete()
        messages.success(request, f'{personnel} retiré(e) du service {service}!')
        return redirect('rh:personnel_service_list')
    
    return render(request, 'rh/personnel_service_delete.html', {'affectation': affectation})
