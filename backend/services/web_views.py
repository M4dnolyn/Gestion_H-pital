from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count

from .models import Service
from .forms import ServiceForm
from personnes.models import Personnel
from rh.models import PersonnelService


# ==================== VUES SERVICES ====================

@login_required
def service_list(request):
    """Liste des services avec recherche"""
    services_list = Service.objects.all().annotate(
        nb_personnel=Count('personnelservice')
    ).order_by('nom_service')
    
    # Recherche
    query = request.GET.get('q')
    if query:
        services_list = services_list.filter(
            Q(nom_service__icontains=query) |
            Q(localisation__icontains=query) |
            Q(description__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(services_list, 12)
    page_number = request.GET.get('page')
    services = paginator.get_page(page_number)
    
    context = {
        'services': services,
        'total_services': Service.objects.count(),
    }
    return render(request, 'services/service_list.html', context)


@login_required
def service_detail(request, pk):
    """Détail d'un service avec son personnel"""
    service = get_object_or_404(Service, pk=pk)
    
    # Récupérer le personnel affecté à ce service
    affectations = PersonnelService.objects.filter(service=service).select_related('personnel')
    personnel = [aff.personnel for aff in affectations]
    
    context = {
        'service': service,
        'personnel': personnel,
        'nb_personnel': len(personnel),
    }
    return render(request, 'services/service_detail.html', context)


@login_required
def service_create(request):
    """Créer un nouveau service"""
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save()
            messages.success(request, f'Service "{service.nom_service}" créé avec succès!')
            return redirect('services:service_detail', pk=service.pk)
    else:
        form = ServiceForm()
    
    return render(request, 'services/service_form.html', {'form': form})


@login_required
def service_update(request, pk):
    """Modifier un service existant"""
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, f'Service "{service.nom_service}" modifié avec succès!')
            return redirect('services:service_detail', pk=service.pk)
    else:
        form = ServiceForm(instance=service)
    
    return render(request, 'services/service_form.html', {
        'form': form,
        'service': service
    })


@login_required
def service_delete(request, pk):
    """Supprimer un service"""
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == 'POST':
        nom = service.nom_service
        service.delete()
        messages.success(request, f'Service "{nom}" supprimé avec succès!')
        return redirect('services:service_list')
    
    return render(request, 'services/service_delete.html', {'service': service})
