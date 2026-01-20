from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RendezVousViewSet
from . import web_views

router = DefaultRouter()
router.register(r'api', RendezVousViewSet, basename='api_rendezvous')

urlpatterns = [
    # API via Router
    path('', include(router.urls)),
    
    # Web Views
    path('', web_views.rendezvous_list, name='rendezvous_list'),
    path('nouveau/', web_views.rendezvous_create, name='rendezvous_create'),
    path('<int:pk>/', web_views.rendezvous_detail, name='rendezvous_detail'),
    path('<int:pk>/modifier/', web_views.rendezvous_update, name='rendezvous_update'),
    path('<int:pk>/supprimer/', web_views.rendezvous_delete, name='rendezvous_delete'),
    path('<int:pk>/annuler/', web_views.rendezvous_cancel, name='rendezvous_cancel'),
    path('<int:pk>/confirmer/', web_views.rendezvous_confirm, name='rendezvous_confirm'),
    path('<int:pk>/terminer/', web_views.rendezvous_complete, name='rendezvous_complete'),
    
    path('calendrier/', web_views.rendezvous_calendar, name='rendezvous_calendar'),
    path('calendrier/api/', web_views.rendezvous_calendar_api, name='rendezvous_calendar_api'),
]
