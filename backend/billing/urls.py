from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrestationViewSet, FactureViewSet, PaiementViewSet, FacturePrestationViewSet
from . import web_views

router = DefaultRouter()
router.register(r'prestations', PrestationViewSet)
router.register(r'factures', FactureViewSet)
router.register(r'paiements', PaiementViewSet)
router.register(r'facture-prestations', FacturePrestationViewSet)

app_name = 'billing'

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
    # Web URLs - Prestations
    path('prestations/', web_views.prestation_list, name='prestation_list'),
    path('prestations/nouvelle/', web_views.prestation_create, name='prestation_create'),
    path('prestations/<int:pk>/modifier/', web_views.prestation_update, name='prestation_update'),
    path('prestations/<int:pk>/supprimer/', web_views.prestation_delete, name='prestation_delete'),
    
    # Web URLs - Factures
    path('factures/', web_views.facture_list, name='facture_list'),
    path('factures/nouvelle/', web_views.facture_create, name='facture_create'),
    path('factures/<int:pk>/', web_views.facture_detail, name='facture_detail'),
    path('factures/<int:pk>/modifier/', web_views.facture_update, name='facture_update'),
    path('factures/<int:pk>/ajouter-ligne/', web_views.facture_add_ligne, name='facture_add_ligne'),
    path('factures/<int:facture_pk>/supprimer-ligne/<int:ligne_pk>/', web_views.facture_delete_ligne, name='facture_delete_ligne'),
    
    # Web URLs - Paiements
    path('factures/<int:facture_pk>/payer/', web_views.paiement_create, name='paiement_create'),
    path('paiements/<int:pk>/', web_views.paiement_detail, name='paiement_detail'),
]
