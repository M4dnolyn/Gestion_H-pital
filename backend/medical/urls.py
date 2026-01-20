from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultationViewSet, OrdonnanceViewSet
from . import web_views


# app_name = 'medical'  <-- DISABLING NAMESPACE

router = DefaultRouter()
router.register(r'consultations', ConsultationViewSet)
router.register(r'ordonnances', OrdonnanceViewSet)

urlpatterns = [
    # API
    path('api/medical/', include(router.urls)),
    
    # Web Views - Ordonnances
    path('ordonnances/', web_views.ordonnance_list, name='ordonnance_list'),
    path('ordonnances/nouvelle/', web_views.ordonnance_create, name='ordonnance_create'),
    path('ordonnances/<int:pk>/', web_views.ordonnance_detail, name='ordonnance_detail'),
    path('ordonnances/<int:pk>/modifier/', web_views.ordonnance_update, name='ordonnance_update'),
    path('ordonnances/<int:pk>/supprimer/', web_views.ordonnance_delete, name='ordonnance_delete'),

    # Web Views - Consultations
    path('consultations/', web_views.consultation_list, name='consultation_list'),
    path('consultations/nouvelle/', web_views.consultation_create, name='consultation_create'),
    path('consultations/<int:pk>/', web_views.consultation_detail, name='consultation_detail'),
    path('consultations/<int:pk>/modifier/', web_views.consultation_update, name='consultation_update'),
    path('consultations/<int:pk>/supprimer/', web_views.consultation_delete, name='consultation_delete'),
]
