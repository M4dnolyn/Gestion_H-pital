from django.urls import path
from . import views, web_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Public
    path('', views.index, name='index'),
    
    # Auth (Redirection vers les vues standard Django mais avec les templates du projet)
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/logout/confirm/', views.logout_confirm, name='logout_confirm'),
    
    # API / Test
    path('api/health/', views.health_check, name='health_check'),

    # Administration
    path('users/create/', web_views.admin_create_user, name='admin_create_user'),
]