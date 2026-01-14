# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Dashboards par rôle
    path('medecin/', views.dashboard_medecin, name='dashboard_medecin'),
    path('infirmier/', views.dashboard_infirmier, name='dashboard_infirmier'),
    path('administratif/', views.dashboard_admin, name='dashboard_admin'),
    
    # Gestion des données
    path('patients/', views.patients_list, name='patients'),
    path('personnel/', views.personnel_list, name='personnel'),
    path('rendezvous/', views.appointments, name='rendezvous'),
    path('consultations/', views.consultations, name='consultations'),
    
    # Authentification
    path('logout/', views.logout_view, name='logout'),
    path('logout/confirm/', views.logout_confirm, name='logout_confirm'),
    
    # Test et santé
    path('test/', views.test_view, name='test'),
    path('health/', views.health_check, name='health_check'),
]