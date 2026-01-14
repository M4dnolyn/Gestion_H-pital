# urls.py (du projet principal)
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Pages publiques
    path('', views.index, name='index'),
    
    # Authentification
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='accounts/logout_confirm.html'), name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/roles/', views.dashboard_roles, name='dashboard_roles'),
    # Patients
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/nouveau/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/modifier/', views.patient_update, name='patient_update'),
    path('patients/<int:pk>/supprimer/', views.patient_delete, name='patient_delete'),
    
    # Rendez-vous
    path('rendezvous/', views.rendezvous_list, name='rendezvous_list'),
    path('rendezvous/nouveau/', views.rendezvous_create, name='rendezvous_create'),
    path('rendezvous/<int:pk>/', views.rendezvous_detail, name='rendezvous_detail'),
    path('rendezvous/<int:pk>/modifier/', views.rendezvous_update, name='rendezvous_update'),
    path('rendezvous/<int:pk>/supprimer/', views.rendezvous_delete, name='rendezvous_delete'),
    path('rendezvous/<int:pk>/annuler/', views.rendezvous_cancel, name='rendezvous_cancel'),
    
    # Consultations
    path('consultations/', views.consultation_list, name='consultation_list'),
    path('consultations/nouvelle/', views.consultation_create, name='consultation_create'),
    path('consultations/<int:pk>/', views.consultation_detail, name='consultation_detail'),
    path('consultations/<int:pk>/modifier/', views.consultation_update, name='consultation_update'),
    path('consultations/<int:pk>/supprimer/', views.consultation_delete, name='consultation_delete'),
    
    # API pour le calendrier
    path('api/rendezvous/calendar/', views.rendezvous_calendar_api, name='rendezvous_calendar_api'),
]
