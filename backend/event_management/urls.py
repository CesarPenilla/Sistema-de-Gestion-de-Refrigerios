from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstudianteViewSet, CodigoQRViewSet

router = DefaultRouter()
router.register(r'estudiantes', EstudianteViewSet, basename='estudiante')
router.register(r'codigos-qr', CodigoQRViewSet, basename='codigoqr')

urlpatterns = [
    path('', include(router.urls)),
]
