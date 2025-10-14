from django.contrib import admin
from .models import Estudiante, CodigoQR


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'identificacion', 'email', 'activo', 'fecha_registro']
    list_filter = ['activo', 'fecha_registro']
    search_fields = ['nombre', 'identificacion', 'email']
    ordering = ['nombre']


@admin.register(CodigoQR)
class CodigoQRAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'tipo_comida', 'codigo', 'usado', 'fecha_creacion', 'fecha_uso']
    list_filter = ['tipo_comida', 'usado', 'fecha_creacion']
    search_fields = ['estudiante__nombre', 'codigo']
    readonly_fields = ['codigo', 'fecha_creacion', 'fecha_uso']
    ordering = ['estudiante', 'tipo_comida']
    
    def has_add_permission(self, request):
        # Los códigos QR se crean automáticamente, no manualmente
        return False
