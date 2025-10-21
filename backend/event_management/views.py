from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Estudiante, CodigoQR
from .serializers import (
    EstudianteSerializer, 
    CodigoQRSerializer, 
    EstudianteConCodigosSerializer,
    ValidarCodigoQRSerializer
)
import qrcode
from io import BytesIO
from django.http import HttpResponse
import base64
from .email_utils import enviar_codigos_qr_email


class EstudianteViewSet(viewsets.ModelViewSet):
    """ViewSet para operaciones CRUD de Estudiantes"""
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer

    def get_queryset(self):
        """Filtra estudiantes activos si se especifica en los parámetros"""
        queryset = Estudiante.objects.all()
        solo_activos = self.request.query_params.get('activos', None)
        if solo_activos == 'true':
            queryset = queryset.filter(activo=True)
        return queryset

    @action(detail=True, methods=['get'])
    def con_codigos(self, request, pk=None):
        """Obtiene un estudiante con todos sus códigos QR"""
        estudiante = self.get_object()
        serializer = EstudianteConCodigosSerializer(estudiante)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def generar_codigos(self, request, pk=None):
        """Genera los 3 códigos QR para un estudiante (desayuno, almuerzo, refrigerio)"""
        estudiante = self.get_object()
        
        # Verificar si el estudiante está activo
        if not estudiante.activo:
            return Response(
                {'error': 'No se pueden generar códigos para estudiantes inactivos.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar si ya tiene códigos
        codigos_existentes = CodigoQR.objects.filter(estudiante=estudiante)
        if codigos_existentes.exists():
            return Response(
                {'error': 'Este estudiante ya tiene códigos QR generados.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear los 3 códigos QR
        tipos_comida = ['DESAYUNO', 'ALMUERZO', 'REFRIGERIO']
        codigos_creados = []
        
        for tipo in tipos_comida:
            codigo_qr = CodigoQR.objects.create(
                estudiante=estudiante,
                tipo_comida=tipo,
                visitante_id=estudiante.identificacion,
                visitante_nombre=estudiante.nombre,
                visitante_identificacion=estudiante.identificacion,
                visitante_email=estudiante.email
            )
            codigos_creados.append(codigo_qr)
        
        # Enviar códigos QR por email
        email_enviado = enviar_codigos_qr_email(estudiante, codigos_creados)
        
        serializer = CodigoQRSerializer(codigos_creados, many=True)
        mensaje = f'Se generaron {len(codigos_creados)} códigos QR exitosamente.'
        if email_enviado:
            mensaje += f' Se enviaron al correo: {estudiante.email}'
        else:
            mensaje += ' No se pudo enviar el email. Por favor verifica la configuración.'
        
        return Response(
            {
                'mensaje': mensaje,
                'email_enviado': email_enviado,
                'codigos': serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'])
    def generar_codigos_masivo(self, request):
        """Genera códigos QR para todos los estudiantes activos que no tengan códigos"""
        # Obtener estudiantes activos sin códigos QR
        estudiantes_sin_codigos = Estudiante.objects.filter(
            activo=True
        ).exclude(
            codigos_qr__isnull=False
        ).distinct()
        
        if not estudiantes_sin_codigos.exists():
            return Response(
                {
                    'mensaje': 'No hay estudiantes activos sin códigos QR.',
                    'estudiantes_procesados': 0
                },
                status=status.HTTP_200_OK
            )
        
        tipos_comida = ['DESAYUNO', 'ALMUERZO', 'REFRIGERIO']
        total_codigos = 0
        estudiantes_procesados = []
        emails_enviados = 0
        emails_fallidos = 0
        
        for estudiante in estudiantes_sin_codigos:
            # Verificar nuevamente que no tenga códigos
            if not CodigoQR.objects.filter(estudiante=estudiante).exists():
                codigos_creados = []
                for tipo in tipos_comida:
                    codigo = CodigoQR.objects.create(
                        estudiante=estudiante,
                        tipo_comida=tipo,
                        visitante_id=estudiante.identificacion,
                        visitante_nombre=estudiante.nombre,
                        visitante_identificacion=estudiante.identificacion,
                        visitante_email=estudiante.email
                    )
                    codigos_creados.append(codigo)
                    total_codigos += 1
                
                # Enviar email con los códigos
                if enviar_codigos_qr_email(estudiante, codigos_creados):
                    emails_enviados += 1
                else:
                    emails_fallidos += 1
                
                estudiantes_procesados.append({
                    'id': estudiante.id,
                    'nombre': estudiante.nombre,
                    'identificacion': estudiante.identificacion,
                    'email': estudiante.email
                })
        
        mensaje = f'Se generaron códigos QR para {len(estudiantes_procesados)} estudiantes.'
        if emails_enviados > 0:
            mensaje += f' Se enviaron {emails_enviados} emails exitosamente.'
        if emails_fallidos > 0:
            mensaje += f' {emails_fallidos} emails fallaron.'
        
        return Response(
            {
                'mensaje': mensaje,
                'total_codigos_generados': total_codigos,
                'estudiantes_procesados': estudiantes_procesados,
                'emails_enviados': emails_enviados,
                'emails_fallidos': emails_fallidos
            },
            status=status.HTTP_201_CREATED
        )


class CodigoQRViewSet(viewsets.ModelViewSet):
    """ViewSet para operaciones CRUD de Códigos QR"""
    queryset = CodigoQR.objects.all()
    serializer_class = CodigoQRSerializer

    @action(detail=False, methods=['post'])
    def validar(self, request):
        """Valida y marca un código QR como usado"""
        serializer = ValidarCodigoQRSerializer(data=request.data)
        
        if serializer.is_valid():
            codigo_uuid = serializer.validated_data['codigo']
            codigo_qr = get_object_or_404(CodigoQR, codigo=codigo_uuid)
            
            if codigo_qr.usado:
                return Response(
                    {
                        'error': 'Este código QR ya ha sido utilizado.',
                        'fecha_uso': codigo_qr.fecha_uso
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Marcar como usado
            codigo_qr.marcar_como_usado()
            
            # Usar visitante_nombre si existe, sino estudiante
            nombre = codigo_qr.visitante_nombre if codigo_qr.visitante_nombre else (codigo_qr.estudiante.nombre if codigo_qr.estudiante else 'Desconocido')
            
            return Response(
                {
                    'mensaje': 'Código QR validado exitosamente.',
                    'estudiante': nombre,
                    'tipo_comida': codigo_qr.tipo_comida,
                    'fecha_uso': codigo_qr.fecha_uso
                },
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def generar_imagen(self, request, pk=None):
        """Genera la imagen del código QR"""
        codigo_qr_obj = self.get_object()
        
        # Crear el código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Datos del QR: incluye el UUID del código
        qr_data = str(codigo_qr_obj.codigo)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Crear la imagen
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir a bytes
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Retornar la imagen
        return HttpResponse(buffer, content_type='image/png')

    @action(detail=True, methods=['get'])
    def generar_base64(self, request, pk=None):
        """Genera el código QR en formato base64"""
        codigo_qr_obj = self.get_object()
        
        # Crear el código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        qr_data = str(codigo_qr_obj.codigo)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Convertir a base64
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        nombre = codigo_qr_obj.visitante_nombre if codigo_qr_obj.visitante_nombre else (codigo_qr_obj.estudiante.nombre if codigo_qr_obj.estudiante else 'Desconocido')
        
        return Response({
            'codigo': str(codigo_qr_obj.codigo),
            'tipo_comida': codigo_qr_obj.tipo_comida,
            'estudiante': nombre,
            'imagen_base64': f'data:image/png;base64,{img_base64}'
        })

    @action(detail=False, methods=['get'])
    def por_estudiante(self, request):
        """Obtiene los códigos QR de un estudiante/visitante específico"""
        estudiante_id = request.query_params.get('estudiante_id')
        
        if not estudiante_id:
            return Response(
                {'error': 'Se requiere el parámetro estudiante_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Buscar por visitante_id primero, sino por estudiante_id
        codigos = CodigoQR.objects.filter(visitante_id=estudiante_id)
        if not codigos.exists():
            codigos = CodigoQR.objects.filter(estudiante_id=estudiante_id)
        serializer = self.get_serializer(codigos, many=True)
        return Response(serializer.data)
