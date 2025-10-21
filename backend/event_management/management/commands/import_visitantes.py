from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections, transaction
from event_management.models import Estudiante, CodigoQR
from event_management.email_utils import enviar_codigos_qr_email
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Importar visitantes desde una base MySQL externa (rica_univalle) y crear estudiantes; opcionalmente generar códigos y enviar emails.'

    def add_arguments(self, parser):
        parser.add_argument('--host', required=True, help='Host MySQL de la BD fuente')
        parser.add_argument('--user', required=True, help='Usuario MySQL')
        parser.add_argument('--password', required=False, help='Password MySQL')
        parser.add_argument('--db', required=True, help='Nombre de la base de datos (ej: rica_univalle)')
        parser.add_argument('--port', default='3306', help='Puerto MySQL')
        parser.add_argument('--table', default='visitantes', help='Nombre de la tabla a importar')
        parser.add_argument('--name-field', default='', help='Nombre de la columna con el nombre (si se omite intenta autodetectar)')
        parser.add_argument('--id-field', default='', help='Nombre de la columna con la identificación')
        parser.add_argument('--email-field', default='', help='Nombre de la columna con el email')
        parser.add_argument('--activo-field', default='', help='Nombre de la columna que indica activo (opcional)')
        parser.add_argument('--limit', type=int, default=0, help='Limitar número de filas a importar (0 = todos)')
        parser.add_argument('--dry-run', action='store_true', help='No escribir nada en la DB, solo mostrar lo que se haría')
        parser.add_argument('--generate-codes', action='store_true', help='Generar códigos QR para cada estudiante importado')
        parser.add_argument('--send-emails', action='store_true', help='Enviar emails con los códigos (requiere generate-codes)')

    def handle(self, *args, **options):
        # Añadir configuración temporal de la DB origen
        rica_cfg = {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': options['db'],
            'USER': options['user'],
            'PASSWORD': options.get('password') or '',
            'HOST': options['host'],
            'PORT': options['port'],
        }

        settings.DATABASES['rica_source'] = rica_cfg

        table = options['table']
        limit = options['limit']
        dry_run = options['dry_run']
        generate_codes = options['generate_codes']
        send_emails = options['send_emails']

        if send_emails and not generate_codes:
            self.stdout.write(self.style.WARNING('--send-emails activa --generate-codes también (se requiere).'))
            return

        # Query the source DB
        with connections['rica_source'].cursor() as cursor:
            sql = f"SELECT * FROM `{table}`"
            if limit and limit > 0:
                sql += f" LIMIT {limit}"
            try:
                cursor.execute(sql)
            except Exception as e:
                self.stderr.write(f'Error al consultar la tabla {table}: {e}')
                return

            cols = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        self.stdout.write(f'Filas encontradas: {len(rows)}')

        # Heurística para detectar columnas si no se especificaron
        def find_field(candidates):
            for c in candidates:
                if c in cols:
                    return c
            return None

        name_field = options['name_field'] or find_field(['nombre', 'nombre_completo', 'full_name', 'name', 'visitante'])
        id_field = options['id_field'] or find_field(['identificacion', 'documento', 'id_number', 'dni'])
        email_field = options['email_field'] or find_field(['email', 'correo', 'correo_electronico'])
        activo_field = options['activo_field'] or find_field(['activo', 'status', 'estado', 'is_active'])

        if not email_field:
            self.stderr.write('No se pudo detectar la columna de email. Usa --email-field para indicar el nombre de la columna.')
            return

        created = 0
        skipped = 0

        for row in rows:
            record = dict(zip(cols, row))

            nombre = record.get(name_field) if name_field else None
            identificacion = record.get(id_field) if id_field else None
            email = record.get(email_field)
            activo = True
            if activo_field:
                activo = bool(record.get(activo_field))

            if not email:
                skipped += 1
                self.stdout.write(self.style.WARNING(f'Se saltó fila sin email: {record}'))
                continue

            # Normalizar email como string
            email = str(email).strip()

            # Si ya existe un estudiante con ese email, omitir
            if Estudiante.objects.filter(email__iexact=email).exists():
                skipped += 1
                self.stdout.write(self.style.NOTICE(f'Estudiante con email {email} ya existe.'))
                continue

            if dry_run:
                self.stdout.write(self.style.SUCCESS(f'[DRY] Crear Estudiante: nombre={nombre} identificacion={identificacion} email={email} activo={activo}'))
                created += 1
                continue

            # Crear estudiante dentro de transacción
            try:
                with transaction.atomic():
                    est = Estudiante.objects.create(
                        nombre=nombre or f'Visitante {email}',
                        identificacion=identificacion or '',
                        email=email,
                        activo=activo,
                    )

                    created += 1

                    # Generar códigos si solicitado
                    codigos_creados = []
                    if generate_codes:
                        tipos = ['DESAYUNO', 'ALMUERZO', 'REFRIGERIO']
                        for tipo in tipos:
                            if not CodigoQR.objects.filter(estudiante=est, tipo_comida=tipo).exists():
                                codigo = CodigoQR.objects.create(estudiante=est, tipo_comida=tipo)
                                codigos_creados.append(codigo)

                        if send_emails and codigos_creados:
                            ok = enviar_codigos_qr_email(est, codigos_creados)
                            if ok:
                                self.stdout.write(self.style.SUCCESS(f'Email enviado a {email}'))
                            else:
                                self.stderr.write(f'Error al enviar email a {email}. Revisa configuración de correo.')

            except Exception as e:
                logger.exception('Error creando estudiante: %s', e)
                self.stderr.write(f'Error al crear estudiante para fila {record}: {e}')

        self.stdout.write(self.style.SUCCESS(f'Import completed: created={created} skipped={skipped}'))
