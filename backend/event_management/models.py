from django.db import models
import uuid
from django.utils import timezone


class Visitante(models.Model):
    """
    Modelo que mapea la tabla 'visitantes' de la base de datos rica_univalle.
    Esta tabla es gestionada por otro software y es de SOLO LECTURA desde Django.
    """
    documento = models.CharField(max_length=50, primary_key=True, db_column='documento')
    nombre = models.CharField(max_length=50, verbose_name="Nombre", db_column='nombre', blank=True, null=True)
    apellido = models.CharField(max_length=50, verbose_name="Apellido", db_column='apellido', blank=True, null=True)
    tipodocumento = models.CharField(max_length=50, verbose_name="Tipo Documento", db_column='tipodocumento', blank=True, null=True)
    dependencia = models.CharField(max_length=50, verbose_name="Dependencia", db_column='dependencia', blank=True, null=True)
    telefono = models.CharField(max_length=50, verbose_name="Teléfono", db_column='telefono', blank=True, null=True)
    funcionario = models.CharField(max_length=50, verbose_name="Funcionario", db_column='funcionario', blank=True, null=True)
    email = models.CharField(max_length=50, verbose_name="Email", db_column='email', blank=True, null=True)
    
    class Meta:
        managed = False  # Django NO creará/modificará esta tabla
        db_table = 'visitantes'  # Nombre exacto de la tabla en rica_univalle
        verbose_name = "Visitante"
        verbose_name_plural = "Visitantes"
        ordering = ['nombre']

    def __str__(self):
        nombre_completo = f"{self.nombre or ''} {self.apellido or ''}".strip()
        return f"{nombre_completo} - {self.documento}"
    
    @property
    def identificacion(self):
        """Propiedad para compatibilidad con la interfaz"""
        return self.documento
    
    @property
    def activo(self):
        """Propiedad para compatibilidad con la interfaz - todos activos"""
        return True
    
    @property
    def fecha_registro(self):
        """Propiedad para compatibilidad"""
        return None
    
    @property
    def nombre_completo(self):
        """Retorna nombre completo combinando nombre y apellido"""
        return f"{self.nombre or ''} {self.apellido or ''}".strip() or self.documento


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
    
    # Relación con Estudiante (mantener por compatibilidad)
    estudiante = models.ForeignKey(
        Estudiante, 
        on_delete=models.CASCADE, 
        related_name='codigos_qr',
        verbose_name="Estudiante",
        null=True,
        blank=True
    )
    
    # Información del visitante (almacenada localmente para auditoría)
    visitante_id = models.CharField(max_length=50, verbose_name="ID Visitante (Documento)", null=True, blank=True)
    visitante_nombre = models.CharField(max_length=200, verbose_name="Nombre Visitante", default='')
    visitante_identificacion = models.CharField(max_length=50, verbose_name="Identificación Visitante", default='')
    visitante_email = models.EmailField(verbose_name="Email Visitante", default='noemail@example.com')
    
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
        unique_together = [['visitante_email', 'tipo_comida']]  # Cambio: usar email en lugar de FK
        ordering = ['visitante_nombre', 'tipo_comida']

    def __str__(self):
        estado = "Usado" if self.usado else "Disponible"
        return f"{self.visitante_nombre} - {self.tipo_comida} ({estado})"

    def marcar_como_usado(self):
        """Marca el código QR como usado"""
        if not self.usado:
            self.usado = True
            self.fecha_uso = timezone.now()
            self.save()
            return True
        return False
