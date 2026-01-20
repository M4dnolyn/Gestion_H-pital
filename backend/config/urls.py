# urls.py (du projet principal)
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
# from . import views  <-- REMOVED (Replaced by core/views.py via include)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core (Index, Dashboard, Auth)
    path('', include('core.urls')),
    
    # Modules Métier (Architecture Modulaire)
    # Note: On garde les noms de module 'personnes', 'medical', etc.
    # Les URL finales seront /personnes/patients/, /medical/consultations/ etc.
    
    # IMPORTANT: Pour la compatibilité avec les anciens templates, on a 
    # déplacé les routes /patients/, /rendezvous/ etc DANS les apps respectives.
    # Ici on utilise include() pour déléguer. D'où path('', include(...)) pour certains si nécessaire,
    # ou mieux, on charge explicitement les patterns.
    
    # En fait, pour respecter l'ancien schéma URL (/patients/, /rendezvous/) sans préfixe d'app forcé,
    # on a deux choix :
    # 1. Utiliser include('personnes.urls') à la racine path('', ...) -> risque de conflit
    # 2. Utiliser des préfixes explicites path('personnes/', ...) -> change les URL (ex: /personnes/patients/)
    
    # D'après ma lecture des urls.py modifiés :
    # planning/urls.py : path('', web_views.rendezvous_list) si préfixé par 'rendezvous/' dans config.
    # personnes/urls.py : path('patients/', ...)
    
    # STRATEGIE HYBRIDE POUR COMPATIBILITÉ MAXIMALE :
    
    # 1. Planning (Rendez-vous)
    # Dans planning/urls.py j'ai mis path('', ...) donc il faut le charger sous 'rendezvous/'
    path('rendezvous/', include('planning.urls')), 
    
    # 2. Medical (Consultations & Ordonnances)
    # Dans medical/urls.py j'ai mis path('consultations/', ...), path('ordonnances/'...)
    # Donc on doit l'inclure à la racine ou sous 'medical/' ?
    # Si je mets path('medical/', include('medical.urls')), l'URL devient /medical/consultations/.
    # L'ancien était /consultations/.
    
    # Pour garder /consultations/ à la racine, je dois inclure medical.urls à la racine,
    # MAIS medical.urls a déjà les préfixes 'consultations/' et 'ordonnances/' dedans?
    # Vérifions : Oui, j'ai mis path('consultations/', ...) dans medical/urls.py.
    # Donc il faut faire :
    path('', include('medical.urls')),
    
    # 3. Personnes (Patients, Personnel)
    # J'ai mis path('patients/', ...) dans personnes/urls.py
    # Donc il faut inclure à la racine pour avoir /patients/ (et pas /personnes/patients/)
    path('', include('personnes.urls')),
    path('personnes/', include('personnes.urls')), # COMPATIBILITÉ: Restaure /personnes/proches/ et /personnes/personnel/
    
    # 4. Facturation (Billing)
    # Lui était déjà sous 'facturation/'
    path('facturation/', include('billing.urls')),
    
    # 5. RH & Services (Déjà préfixés)
    path('rh/', include('rh.urls')),
    path('services/', include('services.urls')),
    
    # Medical Compatibility
    path('medical/', include('medical.urls')), # COMPATIBILITÉ
    
    # NOTE: L'inclusion multiple à '' (racine) fonctionne tant que les sous-patterns sont distincts.
    # medical.urls commence par 'consultations/' ou 'ordonnances/'
    # personnes.urls commence par 'patients/', 'personnel/', 'proches/'
    # C'est parfait, pas de conflit.
]
