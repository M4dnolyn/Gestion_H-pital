from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CongeViewSet, PersonnelServiceViewSet
from . import web_views

router = DefaultRouter()
router.register(r'conges', CongeViewSet)
router.register(r'personnel-services', PersonnelServiceViewSet)

app_name = 'rh'

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
    # Web URLs - Congés
    path('conges/', web_views.conge_list, name='conge_list'),
    path('conges/nouveau/', web_views.conge_create, name='conge_create'),
    path('conges/<int:pk>/', web_views.conge_detail, name='conge_detail'),
    path('conges/<int:pk>/modifier/', web_views.conge_update, name='conge_update'),
    path('conges/<int:pk>/supprimer/', web_views.conge_delete, name='conge_delete'),
    path('conges/<int:pk>/approuver/', web_views.conge_approve, name='conge_approve'),
    path('conges/<int:pk>/refuser/', web_views.conge_reject, name='conge_reject'),
    
    # Web URLs - Personnel-Service
    path('affectations/', web_views.personnel_service_list, name='personnel_service_list'),
    path('affectations/nouvelle/', web_views.personnel_service_create, name='personnel_service_create'),
    path('affectations/<int:pk>/supprimer/', web_views.personnel_service_delete, name='personnel_service_delete'),
]
