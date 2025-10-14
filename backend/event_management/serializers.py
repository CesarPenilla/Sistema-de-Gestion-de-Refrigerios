from rest_framework import serializers
from .models import Estudiante, CodigoQR
import uuid
import re


class EstudianteSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Estudiante"""
    
    class Meta:
        model = Estudiante
        fields = ['id', 'nombre', 'identificacion', 'email', 'activo', 'fecha_registro']
        read_only_fields = ['id', 'fecha_registro']


class CodigoQRSerializer(serializers.ModelSerializer):
    """Serializador para el modelo CodigoQR"""
    estudiante_nombre = serializers.CharField(source='estudiante.nombre', read_only=True)
    codigo_str = serializers.CharField(source='codigo', read_only=True)
    
    class Meta:
        model = CodigoQR
        fields = [
            'id', 
            'estudiante', 
            'estudiante_nombre',
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
