from rest_framework import serializers
from .models import Estudiante, CodigoQR, Visitante
import uuid
import re


class VisitanteSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Visitante (tabla externa)"""
    id = serializers.CharField(source='documento', read_only=True)
    nombre = serializers.SerializerMethodField()
    identificacion = serializers.CharField(source='documento', read_only=True)
    activo = serializers.SerializerMethodField()
    fecha_registro = serializers.SerializerMethodField()
    
    class Meta:
        model = Visitante
        fields = ['id', 'nombre', 'identificacion', 'email', 'activo', 'fecha_registro']
        read_only_fields = ['id', 'nombre', 'identificacion', 'email']
    
    def get_nombre(self, obj):
        """Retorna nombre completo combinando nombre y apellido"""
        return obj.nombre_completo
    
    def get_activo(self, obj):
        return obj.activo
    
    def get_fecha_registro(self, obj):
        return obj.fecha_registro


class EstudianteSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Estudiante"""
    
    class Meta:
        model = Estudiante
        fields = ['id', 'nombre', 'identificacion', 'email', 'activo', 'fecha_registro']
        read_only_fields = ['id', 'fecha_registro']


class CodigoQRSerializer(serializers.ModelSerializer):
    """Serializador para el modelo CodigoQR"""
    estudiante_nombre = serializers.CharField(source='visitante_nombre', read_only=True)
    codigo_str = serializers.CharField(source='codigo', read_only=True)
    
    class Meta:
        model = CodigoQR
        fields = [
            'id', 
            'estudiante', 
            'estudiante_nombre',
            'visitante_id',
            'visitante_nombre',
            'visitante_identificacion',
            'visitante_email',
            'tipo_comida', 
            'codigo',
            'codigo_str',
            'usado', 
            'fecha_creacion', 
            'fecha_uso'
        ]
        read_only_fields = ['id', 'codigo', 'fecha_creacion', 'fecha_uso']


class EstudianteConCodigosSerializer(serializers.ModelSerializer):
    """Serializador de Estudiante con sus códigos QR"""
    codigos_qr = CodigoQRSerializer(many=True, read_only=True)
    
    class Meta:
        model = Estudiante
        fields = ['id', 'nombre', 'identificacion', 'email', 'activo', 'fecha_registro', 'codigos_qr']
        read_only_fields = ['id', 'fecha_registro']


class ValidarCodigoQRSerializer(serializers.Serializer):
    """Serializador para validar un código QR.

    Este validador acepta cadenas con posibles comillas, espacios u otros
    caracteres accidentales (p. ej. los introducidos por el lector) y los
    normaliza a un UUID antes de verificar la existencia en la base de datos.
    """
    codigo = serializers.CharField()

    def validate_codigo(self, value):
        # Limpiar espacios y comillas que a veces pega el lector
        raw = value.strip()
        # Eliminar comillas simples/dobles
        raw = raw.replace("'", "").replace('"', '')
        # Eliminar cualquier caracter que no sea hex o guion
        cleaned = re.sub(r'[^0-9a-fA-F\-]', '', raw)

        # Intentar convertir a UUID
        try:
            codigo_uuid = uuid.UUID(cleaned)
        except Exception:
            raise serializers.ValidationError("Código QR no válido.")

        # Verificar existencia en la DB
        try:
            codigo_qr = CodigoQR.objects.get(codigo=codigo_uuid)
            if codigo_qr.usado:
                raise serializers.ValidationError("Este código QR ya ha sido utilizado.")
        except CodigoQR.DoesNotExist:
            raise serializers.ValidationError("Código QR no válido.")

        # Retornar UUID serializado (opcional)
        return str(codigo_uuid)
