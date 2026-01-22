from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import date, datetime, timedelta
import json

from .models import RendezVous
from .forms import RendezVousForm
from personnes.models import Patient, Personnel

# ==================== VUES RENDEZ-VOUS ====================

@login_required
def rendezvous_list(request):
    """Liste des rendez-vous avec vue calendrier/liste"""
    view_type = request.GET.get('view', 'list')
    status = request.GET.get('status')
    
    rendezvous_list = RendezVous.objects.all().order_by('-date_rdv', '-heure_rdv')
    
    # Filtres par statut
    today = date.today()
    if status == 'today':
        rendezvous_list = rendezvous_list.filter(date_rdv=today)
    elif status == 'upcoming':
        rendezvous_list = rendezvous_list.filter(date_rdv__gte=today)
    elif status == 'past':
        rendezvous_list = rendezvous_list.filter(date_rdv__lt=today)
    
    # Pagination pour la vue liste
    if view_type == 'list':
        paginator = Paginator(rendezvous_list, 15)
        page_number = request.GET.get('page')
        rendezvous = paginator.get_page(page_number)
    else:
        rendezvous = rendezvous_list
    
    medecins = Personnel.objects.filter(fonction='MED')
    
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
    """Créer un rendez-vous"""
    if request.method == 'POST':
        form = RendezVousForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Rendez-vous programmé avec succès!')
                return redirect('rendezvous_list')
            except Exception as e:
                messages.error(request, f"Erreur technique lors de la programmation : {str(e)}")
        else:
            messages.error(request, 'Erreur lors de la programmation. Veuillez vérifier les informations saisies.')
    else:
        # Pré-remplissage possible via GET (ex: depuis détail patient)
        initial_data = {}
        patient_id = request.GET.get('patient')
        if patient_id:
            initial_data['patient'] = patient_id
        form = RendezVousForm(initial=initial_data)
    
    return render(request, 'rendezvous/form.html', {'form': form})


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
        rdv.statut_rdv = 'Annulé' # Correction consistency (majuscule)
        rdv.save()
        messages.warning(request, 'Rendez-vous annulé!')
        return redirect('rendezvous_detail', pk=rdv.pk)
    
    return render(request, 'rendezvous/cancel.html', {'rdv': rdv})


@login_required
def rendezvous_confirm(request, pk):
    """Confirmer un rendez-vous"""
    rdv = get_object_or_404(RendezVous, pk=pk)
    if request.method == 'POST':
        rdv.statut_rdv = 'Confirmé'
        rdv.save()
        messages.success(request, 'Rendez-vous confirmé.')
        return redirect('rendezvous_detail', pk=rdv.pk)
    return redirect('rendezvous_detail', pk=rdv.pk)

@login_required
def rendezvous_complete(request, pk):
    """Marquer un rendez-vous comme terminé"""
    rdv = get_object_or_404(RendezVous, pk=pk)
    if request.method == 'POST':
        rdv.statut_rdv = 'Terminé'
        rdv.save()
        messages.success(request, 'Rendez-vous marqué comme terminé.')
        return redirect('rendezvous_detail', pk=rdv.pk)
    return redirect('rendezvous_detail', pk=rdv.pk)


@login_required
def rendezvous_calendar(request):
    """Affiche la vue calendrier des rendez-vous"""
    return render(request, 'planning/calendar.html')


@login_required
def rendezvous_calendar_api(request):
    """API pour le calendrier des rendez-vous (format JSON)"""
    start = request.GET.get('start', date.today().isoformat())
    end = request.GET.get('end', (date.today() + timedelta(days=30)).isoformat())
    
    rendezvous = RendezVous.objects.filter(
        date_rdv__gte=start,
        date_rdv__lte=end
    ).select_related('patient', 'medecin')
    
    events = []
    for rdv in rendezvous:
        # Définir la couleur selon le statut
        if rdv.statut_rdv == 'Confirmé':
            color = '#28a745'  # Vert
        elif rdv.statut_rdv == 'Annulé':
            color = '#dc3545'  # Rouge
        elif rdv.statut_rdv == 'Terminé':
            color = '#17a2b8'  # Bleu
        else:
            color = '#6c757d'  # Gris (Programmé)
        
        events.append({
            'id': rdv.id,
            'title': f"{rdv.patient.nom} {rdv.patient.prenom} - Consultation",
            'start': f"{rdv.date_rdv.isoformat()}T{rdv.heure_rdv}",
            'color': color,
            'extendedProps': {
                'patient': str(rdv.patient),
                'medecin': str(rdv.medecin) if rdv.medecin else '',
                'statut': rdv.statut_rdv,
                'motif': rdv.motif or ''
            }
        })
    
    return JsonResponse(events, safe=False)
