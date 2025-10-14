import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from io import BytesIO
import qrcode
from email.mime.image import MIMEImage

logger = logging.getLogger(__name__)


def generar_imagen_qr(codigo_uuid):
    """Genera una imagen QR y la retorna como bytes"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(codigo_uuid))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer.getvalue()


def enviar_codigos_qr_email(estudiante, codigos_qr):
    """
    Envía los códigos QR por email al estudiante
    
    Args:
        estudiante: Objeto Estudiante
        codigos_qr: Lista de objetos CodigoQR
    
    Returns:
        bool: True si se envió correctamente, False en caso contrario
    """
    try:
        # Asunto del email
        subject = f'🎫 Tus Códigos QR para el Evento - {estudiante.nombre}'
        
        # Contenido HTML del email
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background-color: #f9f9f9;
                    padding: 30px;
                    border: 1px solid #ddd;
                }}
                .qr-section {{
                    background-color: white;
                    margin: 20px 0;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    text-align: center;
                }}
                .qr-title {{
                    color: #4CAF50;
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                .qr-image {{
                    max-width: 300px;
                    margin: 15px auto;
                    display: block;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    color: #777;
                    font-size: 12px;
                    border-top: 1px solid #ddd;
                    margin-top: 20px;
                }}
                .important {{
                    background-color: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🍽️ Sistema de Gestión de Refrigerios</h1>
            </div>
            
            <div class="content">
                <h2>¡Hola {estudiante.nombre}!</h2>
                <p>Te enviamos tus códigos QR para el evento. Cada código es de <strong>uso único</strong>.</p>
                
                <div class="important">
                    <strong>⚠️ Importante:</strong>
                    <ul>
                        <li>Cada código QR solo puede usarse <strong>una vez</strong></li>
                        <li>Presenta el código correspondiente en el momento adecuado</li>
                        <li>Guarda este email para tener acceso a tus códigos</li>
                    </ul>
                </div>
                
                <h3>Tus Códigos QR:</h3>
        """
        
        # Crear el email
        email = EmailMultiAlternatives(
            subject=subject,
            body=f'Hola {estudiante.nombre}, adjuntamos tus códigos QR para el evento.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[estudiante.email]
        )
        
        # Agregar cada código QR
        for idx, codigo in enumerate(codigos_qr):
            # Generar imagen QR
            img_data = generar_imagen_qr(codigo.codigo)
            
            # Crear el MIMEImage
            img = MIMEImage(img_data)
            img.add_header('Content-ID', f'<qr_{codigo.tipo_comida}>')
            img.add_header('Content-Disposition', 'inline', 
                          filename=f'QR_{codigo.tipo_comida}.png')
            email.attach(img)
            
            # Agregar sección HTML para este código
            html_content += f"""
                <div class="qr-section">
                    <div class="qr-title">📱 {codigo.tipo_comida}</div>
                    <img src="cid:qr_{codigo.tipo_comida}" class="qr-image" alt="QR {codigo.tipo_comida}">
                    <p style="color: #666; font-size: 14px;">Código: {codigo.codigo}</p>
                </div>
            """
        
        # Cerrar el HTML
        html_content += """
                <div class="footer">
                    <p>Este es un correo automático. Por favor no respondas a este mensaje.</p>
                    <p>Sistema de Gestión de Refrigerios © 2025</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True

    except Exception as e:
        # Registrar la excepción completa para facilitar el diagnóstico
        logger.exception(f"Error al enviar email al estudiante {estudiante.email}: {e}")
        return False


def enviar_notificacion_error(estudiante, error_msg):
    """
    Envía un email notificando que hubo un error
    """
    try:
        subject = f'⚠️ Error al generar códigos QR - {estudiante.nombre}'
        message = f"""
        Hola {estudiante.nombre},
        
        Hubo un problema al generar tus códigos QR:
        {error_msg}
        
        Por favor contacta al administrador del evento.
        
        Saludos,
        Sistema de Gestión de Refrigerios
        """
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[estudiante.email]
        )
        email.send()
        return True

    except Exception as e:
        logger.exception(f"Error al enviar notificación de error al estudiante {estudiante.email}: {e}")
        return False
