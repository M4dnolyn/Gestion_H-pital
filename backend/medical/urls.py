from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultationViewSet, OrdonnanceViewSet

router = DefaultRouter()
router.register(r'consultations', ConsultationViewSet)
router.register(r'ordonnances', OrdonnanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
