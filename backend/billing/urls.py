from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PrestationViewSet, FactureViewSet, PaiementViewSet, FacturePrestationViewSet

router = DefaultRouter()
router.register(r'prestations', PrestationViewSet)
router.register(r'factures', FactureViewSet)
router.register(r'paiements', PaiementViewSet)
router.register(r'facture-prestations', FacturePrestationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
