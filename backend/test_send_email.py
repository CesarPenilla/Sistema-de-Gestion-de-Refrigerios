import sys
import traceback

import os
import django

# Preparar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail

print('EMAIL_HOST:', settings.EMAIL_HOST)
print('EMAIL_PORT:', settings.EMAIL_PORT)
print('EMAIL_HOST_USER:', settings.EMAIL_HOST_USER)
print('EMAIL_HOST_PASSWORD length:', len(getattr(settings, 'EMAIL_HOST_PASSWORD', '')))

try:
    result = send_mail(
        '🧪 Prueba de Email - Sistema Refrigerios',
        'Si recibes este mensaje, la configuración SMTP está correcta.',
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )
    print('send_mail returned:', result)
    print('Si no ves errores, revisa la bandeja de entrada o SPAM de', settings.EMAIL_HOST_USER)
except Exception as exc:
    print('Error al enviar email:')
    traceback.print_exc()
    sys.exit(1)
