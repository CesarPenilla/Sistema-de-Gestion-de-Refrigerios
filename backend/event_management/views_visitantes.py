from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Visitante, CodigoQR
from .serializers import VisitanteSerializer, CodigoQRSerializer
from .email_utils import enviar_codigos_qr_email


class VisitanteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consultar Visitantes desde la BD externa rica_univalle.
    Solo operaciones de lectura (la gestión se hace en el otro software).
    """
    serializer_class = VisitanteSerializer
    
    def get_queryset(self):
        """Obtener visitantes desde la BD externa"""
        queryset = Visitante.objects.using('rica_univalle').all()
        # Filtro opcional por activos (si existe campo en la tabla)
        solo_activos = self.request.query_params.get('activos', None)
        if solo_activos == 'true':
            # Todos los visitantes son considerados activos
            pass
        return queryset
    
    @action(detail=True, methods=['get'])
    def codigos(self, request, pk=None):
        """Obtiene los códigos QR generados para un visitante"""
        visitante = self.get_object()
        # Buscar por email o documento
        if visitante.email:
            codigos = CodigoQR.objects.filter(visitante_email=visitante.email)
        else:
            codigos = CodigoQR.objects.filter(visitante_identificacion=visitante.documento)
        serializer = CodigoQRSerializer(codigos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def generar_codigos(self, request, pk=None):
        """Genera los 3 códigos QR para un visitante (desayuno, almuerzo, refrigerio)"""
        visitante = self.get_object()
        
        # Verificar si ya tiene códigos (buscar por email o documento)
        codigos_existentes = CodigoQR.objects.filter(visitante_email=visitante.email) if visitante.email else CodigoQR.objects.filter(visitante_identificacion=visitante.documento)
        if codigos_existentes.exists():
            return Response(
                {'error': 'Este visitante ya tiene códigos QR generados.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear los 3 códigos QR en la BD local
        tipos_comida = ['DESAYUNO', 'ALMUERZO', 'REFRIGERIO']
        codigos_creados = []
        
        for tipo in tipos_comida:
            codigo_qr = CodigoQR.objects.create(
                visitante_id=visitante.documento,  # Guardamos el documento como visitante_id
                visitante_nombre=visitante.nombre_completo,
                visitante_identificacion=visitante.documento,
                visitante_email=visitante.email or f'{visitante.documento}@noemail.com',
                tipo_comida=tipo
            )
            codigos_creados.append(codigo_qr)
        
        # Crear objeto temporal compatible con la función de email
        class VisitanteEmail:
            def __init__(self, v):
                self.nombre = v.nombre_completo
                self.email = v.email or f'{v.documento}@noemail.com'
                self.identificacion = v.documento
        
        # Enviar códigos QR por email solo si tiene email válido
        email_enviado = False
        if visitante.email:
            email_enviado = enviar_codigos_qr_email(VisitanteEmail(visitante), codigos_creados)
        
        serializer = CodigoQRSerializer(codigos_creados, many=True)
        mensaje = f'Se generaron {len(codigos_creados)} códigos QR exitosamente.'
        if visitante.email:
            if email_enviado:
                mensaje += f' Se enviaron al correo: {visitante.email}'
            else:
                mensaje += ' No se pudo enviar el email. Por favor verifica la configuración.'
        else:
            mensaje += ' No se envió email (visitante sin correo registrado).'
        
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
        """Genera códigos QR para todos los visitantes que no tengan códigos"""
        # Obtener todos los visitantes
        visitantes = Visitante.objects.using('rica_univalle').all()
        
        # Filtrar los que NO tienen códigos
        visitantes_sin_codigos = []
        for v in visitantes:
            # Buscar por email o documento
            if v.email:
                tiene_codigos = CodigoQR.objects.filter(visitante_email=v.email).exists()
            else:
                tiene_codigos = CodigoQR.objects.filter(visitante_identificacion=v.documento).exists()
            
            if not tiene_codigos:
                visitantes_sin_codigos.append(v)
        
        if not visitantes_sin_codigos:
            return Response(
                {
                    'mensaje': 'No hay visitantes sin códigos QR.',
                    'estudiantes_procesados': [],
                    'total_codigos_generados': 0,
                    'emails_enviados': 0,
                    'emails_fallidos': 0
                },
                status=status.HTTP_200_OK
            )
        
        tipos_comida = ['DESAYUNO', 'ALMUERZO', 'REFRIGERIO']
        total_codigos = 0
        visitantes_procesados = []
        emails_enviados = 0
        emails_fallidos = 0
        
        for visitante in visitantes_sin_codigos:
            codigos_creados = []
            for tipo in tipos_comida:
                codigo = CodigoQR.objects.create(
                    visitante_id=visitante.documento,  # Guardamos el documento como visitante_id
                    visitante_nombre=visitante.nombre_completo,
                    visitante_identificacion=visitante.documento,
                    visitante_email=visitante.email or f'{visitante.documento}@noemail.com',
                    tipo_comida=tipo
                )
                codigos_creados.append(codigo)
                total_codigos += 1
            
            # Crear objeto temporal
            class VisitanteEmail:
                def __init__(self, v):
                    self.nombre = v.nombre_completo
                    self.email = v.email or f'{v.documento}@noemail.com'
                    self.identificacion = v.documento
            
            # Enviar email solo si tiene email válido
            if visitante.email:
                if enviar_codigos_qr_email(VisitanteEmail(visitante), codigos_creados):
                    emails_enviados += 1
                else:
                    emails_fallidos += 1
            
            visitantes_procesados.append({
                'id': visitante.documento,
                'nombre': visitante.nombre_completo,
                'identificacion': visitante.documento,
                'email': visitante.email or 'Sin email'
            })
        
        mensaje = f'Se generaron códigos QR para {len(visitantes_procesados)} visitantes.'
        if emails_enviados > 0:
            mensaje += f' Se enviaron {emails_enviados} emails exitosamente.'
        if emails_fallidos > 0:
            mensaje += f' {emails_fallidos} emails fallaron.'
        
        return Response(
            {
                'mensaje': mensaje,
                'total_codigos_generados': total_codigos,
                'estudiantes_procesados': visitantes_procesados,
                'emails_enviados': emails_enviados,
                'emails_fallidos': emails_fallidos
            },
            status=status.HTTP_201_CREATED
        )
