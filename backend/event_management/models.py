from django.db import models
import uuid
from django.utils import timezone


class Estudiante(models.Model):
    """Modelo para representar a los estudiantes/invitados al evento"""
    nombre = models.CharField(max_length=200, verbose_name="Nombre Completo")
    identificacion = models.CharField(max_length=50, unique=True, verbose_name="Número de Identificación")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - {self.identificacion}"


class CodigoQR(models.Model):
    """Modelo para los códigos QR de cada tipo de comida"""
    
    TIPO_COMIDA_CHOICES = [
        ('DESAYUNO', 'Desayuno'),
        ('ALMUERZO', 'Almuerzo'),
        ('REFRIGERIO', 'Refrigerio'),
    ]
    
    estudiante = models.ForeignKey(
        Estudiante, 
        on_delete=models.CASCADE, 
        related_name='codigos_qr',
        verbose_name="Estudiante"
    )
    tipo_comida = models.CharField(
        max_length=20, 
        choices=TIPO_COMIDA_CHOICES,
        verbose_name="Tipo de Comida"
    )
    codigo = models.UUIDField(
        default=uuid.uuid4, 
        editable=False, 
        unique=True,
        verbose_name="Código QR"
    )
    usado = models.BooleanField(default=False, verbose_name="Usado")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_uso = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Uso")
    
    class Meta:
        verbose_name = "Código QR"
        verbose_name_plural = "Códigos QR"
        unique_together = ['estudiante', 'tipo_comida']
        ordering = ['estudiante', 'tipo_comida']

    def __str__(self):
        estado = "Usado" if self.usado else "Disponible"
        return f"{self.estudiante.nombre} - {self.tipo_comida} ({estado})"

    def marcar_como_usado(self):
        """Marca el código QR como usado"""
        if not self.usado:
            self.usado = True
            self.fecha_uso = timezone.now()
            self.save()
            return True
        return False
