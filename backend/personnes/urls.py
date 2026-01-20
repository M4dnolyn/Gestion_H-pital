from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, PersonnelViewSet, ProcheAidantViewSet
from . import web_views

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'personnel', PersonnelViewSet)
router.register(r'proches', ProcheAidantViewSet)


# app_name = 'personnes'  <-- DISABLING NAMESPACE TO MATCH LEGACY TEMPLATES

urlpatterns = [
    # API URLs
    path('api/personnes/', include(router.urls)),
    

    # Web URLs - Patients
    path('patients/', web_views.patient_list, name='patient_list'),
    path('patients/nouveau/', web_views.patient_create, name='patient_create'),
    path('patients/<int:pk>/', web_views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/modifier/', web_views.patient_update, name='patient_update'),
    path('patients/<int:pk>/supprimer/', web_views.patient_delete, name='patient_delete'),

    # Web URLs - Personnel
    path('personnel/', web_views.personnel_list, name='personnel_list'),
    path('personnel/nouveau/', web_views.personnel_create, name='personnel_create'),
    path('personnel/<int:pk>/', web_views.personnel_detail, name='personnel_detail'),
    path('personnel/<int:pk>/modifier/', web_views.personnel_update, name='personnel_update'),
    path('personnel/<int:pk>/supprimer/', web_views.personnel_delete, name='personnel_delete'),
    
    # Web URLs - Proches Aidants
    path('proches/', web_views.proche_list, name='proche_list'),
    path('proches/nouveau/', web_views.proche_create, name='proche_create'),
    path('proches/<int:pk>/', web_views.proche_detail, name='proche_detail'),
    path('proches/<int:pk>/modifier/', web_views.proche_update, name='proche_update'),
    path('proches/<int:pk>/supprimer/', web_views.proche_delete, name='proche_delete'),
]
