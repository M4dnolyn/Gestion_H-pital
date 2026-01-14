from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CongeViewSet, PersonnelServiceViewSet

router = DefaultRouter()
router.register(r'conges', CongeViewSet)
router.register(r'personnel-services', PersonnelServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
