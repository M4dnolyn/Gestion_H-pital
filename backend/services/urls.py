from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet
from . import web_views

router = DefaultRouter()
router.register(r'services', ServiceViewSet)

app_name = 'services'

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
    # Web URLs - Services
    path('', web_views.service_list, name='service_list'),
    path('nouveau/', web_views.service_create, name='service_create'),
    path('<int:pk>/', web_views.service_detail, name='service_detail'),
    path('<int:pk>/modifier/', web_views.service_update, name='service_update'),
    path('<int:pk>/supprimer/', web_views.service_delete, name='service_delete'),
]
