from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, PersonnelViewSet, ProcheAidantViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'personnel', PersonnelViewSet)
router.register(r'proches', ProcheAidantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
