from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstudianteViewSet, CodigoQRViewSet
from .views_visitantes import VisitanteViewSet

router = DefaultRouter()
# Usar VisitanteViewSet para el endpoint de estudiantes (lee de rica_univalle)
router.register(r'estudiantes', VisitanteViewSet, basename='estudiante')
router.register(r'codigos-qr', CodigoQRViewSet, basename='codigoqr')

urlpatterns = [
    path('', include(router.urls)),
]
