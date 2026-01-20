from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, F
from django.http import JsonResponse
from datetime import date

from .models import Facture, Paiement, Prestation, FacturePrestation
from .forms import FactureForm, PaiementForm, PrestationForm, FacturePrestationForm
from personnes.models import Patient


# ==================== VUES PRESTATIONS ====================

@login_required
def prestation_list(request):
    """Liste des prestations avec recherche et pagination"""
    prestations_list = Prestation.objects.all().order_by('libelle_acte')
    
    # Recherche
    query = request.GET.get('q')
    if query:
        prestations_list = prestations_list.filter(
            Q(libelle_acte__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(prestations_list, 15)
    page_number = request.GET.get('page')
    prestations = paginator.get_page(page_number)
    
    context = {
        'prestations': prestations,
        'total_prestations': Prestation.objects.count(),
    }
    return render(request, 'billing/prestation_list.html', context)


@login_required
def prestation_create(request):
    """Créer une nouvelle prestation"""
    if request.method == 'POST':
        form = PrestationForm(request.POST)
        if form.is_valid():
            prestation = form.save()
            messages.success(request, f'Prestation "{prestation.libelle_acte}" créée avec succès!')
            return redirect('billing:prestation_list')
    else:
        form = PrestationForm()
    
    return render(request, 'billing/prestation_form.html', {'form': form})


@login_required
def prestation_update(request, pk):
    """Modifier une prestation existante"""
    prestation = get_object_or_404(Prestation, pk=pk)
    
    if request.method == 'POST':
        form = PrestationForm(request.POST, instance=prestation)
        if form.is_valid():
            form.save()
            messages.success(request, f'Prestation "{prestation.libelle_acte}" modifiée avec succès!')
            return redirect('billing:prestation_list')
    else:
        form = PrestationForm(instance=prestation)
    
    return render(request, 'billing/prestation_form.html', {
        'form': form,
        'prestation': prestation
    })


@login_required
def prestation_delete(request, pk):
    """Supprimer une prestation"""
    prestation = get_object_or_404(Prestation, pk=pk)
    
    if request.method == 'POST':
        libelle = prestation.libelle_acte
        prestation.delete()
        messages.success(request, f'Prestation "{libelle}" supprimée avec succès!')
        return redirect('billing:prestation_list')
    
    return render(request, 'billing/prestation_delete.html', {'prestation': prestation})


# ==================== VUES FACTURES ====================

@login_required
def facture_list(request):
    """Liste des factures avec filtres"""
    factures_list = Facture.objects.all().order_by('-date_facture')
    
    # Filtres
    statut = request.GET.get('statut')
    patient_id = request.GET.get('patient')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    
    if statut:
        factures_list = factures_list.filter(statut_paiement=statut)
    if patient_id:
        factures_list = factures_list.filter(patient_id=patient_id)
    if date_debut:
        factures_list = factures_list.filter(date_facture__gte=date_debut)
    if date_fin:
        factures_list = factures_list.filter(date_facture__lte=date_fin)
    
    # Pagination
    paginator = Paginator(factures_list, 15)
    page_number = request.GET.get('page')
    factures = paginator.get_page(page_number)
    
    # Statistiques
    today = date.today()
    context = {
        'factures': factures,
        'patients': Patient.objects.all(),
        'total_factures': Facture.objects.count(),
        'factures_en_attente': Facture.objects.filter(statut_paiement='En attente').count(),
        'factures_payees': Facture.objects.filter(statut_paiement='Payée').count(),
        'factures_aujourdhui': Facture.objects.filter(date_facture=today).count(),
    }
    return render(request, 'billing/facture_list.html', context)


@login_required
def facture_detail(request, pk):
    """Détail d'une facture avec ses lignes"""
    facture = get_object_or_404(Facture, pk=pk)
    lignes = facture.lignes.all().select_related('prestation')
    
    # Calculer le total
    total = sum(ligne.qte * ligne.prix_unit for ligne in lignes)
    
    context = {
        'facture': facture,
        'lignes': lignes,
        'total': total,
    }
    return render(request, 'billing/facture_detail.html', context)


@login_required
def facture_create(request):
    """Créer une nouvelle facture"""
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            facture = form.save()
            messages.success(request, f'Facture #{facture.id} créée avec succès!')
            return redirect('billing:facture_detail', pk=facture.pk)
    else:
        form = FactureForm()
    
    return render(request, 'billing/facture_form.html', {'form': form})


@login_required
def facture_update(request, pk):
    """Modifier une facture existante"""
    facture = get_object_or_404(Facture, pk=pk)
    
    if request.method == 'POST':
        form = FactureForm(request.POST, instance=facture)
        if form.is_valid():
            form.save()
            messages.success(request, f'Facture #{facture.id} modifiée avec succès!')
            return redirect('billing:facture_detail', pk=facture.pk)
    else:
        form = FactureForm(instance=facture)
    
    return render(request, 'billing/facture_form.html', {
        'form': form,
        'facture': facture
    })


@login_required
def facture_add_ligne(request, pk):
    """Ajouter une ligne de prestation à une facture"""
    facture = get_object_or_404(Facture, pk=pk)
    
    if request.method == 'POST':
        form = FacturePrestationForm(request.POST)
        if form.is_valid():
            ligne = form.save(commit=False)
            ligne.facture = facture
            ligne.save()
            messages.success(request, 'Prestation ajoutée à la facture!')
            return redirect('billing:facture_detail', pk=facture.pk)
    else:
        form = FacturePrestationForm()
    
    return render(request, 'billing/facture_add_ligne.html', {
        'form': form,
        'facture': facture
    })


@login_required
def facture_delete_ligne(request, facture_pk, ligne_pk):
    """Supprimer une ligne de facture"""
    facture = get_object_or_404(Facture, pk=facture_pk)
    ligne = get_object_or_404(FacturePrestation, pk=ligne_pk, facture=facture)
    
    if request.method == 'POST':
        ligne.delete()
        messages.success(request, 'Ligne supprimée de la facture!')
        return redirect('billing:facture_detail', pk=facture.pk)
    
    return render(request, 'billing/facture_delete_ligne.html', {
        'facture': facture,
        'ligne': ligne
    })


# ==================== VUES PAIEMENTS ====================

@login_required
def paiement_create(request, facture_pk):
    """Enregistrer un paiement pour une facture"""
    facture = get_object_or_404(Facture, pk=facture_pk)
    
    # Vérifier si un paiement existe déjà
    if hasattr(facture, 'paiement'):
        messages.warning(request, 'Cette facture a déjà été payée!')
        return redirect('billing:facture_detail', pk=facture.pk)
    
    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.facture = facture
            paiement.save()
            
            # Mettre à jour le statut de la facture
            facture.statut_paiement = 'Payée'
            facture.save()
            
            messages.success(request, f'Paiement enregistré avec succès!')
            return redirect('billing:facture_detail', pk=facture.pk)
    else:
        # Calculer le montant total de la facture
        total = sum(ligne.qte * ligne.prix_unit for ligne in facture.lignes.all())
        form = PaiementForm(initial={
            'facture': facture,
            'date_paiement': date.today(),
            'montant_paye': total
        })
    
    return render(request, 'billing/paiement_form.html', {
        'form': form,
        'facture': facture
    })


@login_required
def paiement_detail(request, pk):
    """Détail d'un paiement"""
    paiement = get_object_or_404(Paiement, pk=pk)
    
    return render(request, 'billing/paiement_detail.html', {'paiement': paiement})
