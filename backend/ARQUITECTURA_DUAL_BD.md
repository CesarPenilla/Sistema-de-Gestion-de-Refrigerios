# Arquitectura de Doble Base de Datos

## Resumen
El sistema ahora funciona con **dos bases de datos**:

### 1. `rica_univalle` (Base de datos externa)
- **Propósito**: BD gestionada por otro software donde se registran los visitantes
- **Tabla principal**: `visitantes`
- **Acceso desde Django**: Solo lectura
- **Ubicación**: localhost:3306

### 2. `refrigerio_db` (Base de datos local)
- **Propósito**: BD local donde se almacenan códigos QR y control de uso
- **Tablas principales**: `CodigoQR`, `Estudiante` (para compatibilidad)
- **Acceso desde Django**: Lectura y escritura
- **Ubicación**: localhost:3306

## Flujo de Trabajo

1. **Consulta de visitantes**: 
   - El frontend llama a `/api/estudiantes/`
   - Django consulta la tabla `visitantes` de `rica_univalle`
   - Se muestra la lista en el frontend

2. **Generación de códigos QR**:
   - Usuario selecciona un visitante
   - Se generan 3 códigos (DESAYUNO, ALMUERZO, REFRIGERIO)
   - Los códigos se guardan en `refrigerio_db` con la información del visitante
   - Se envía email automáticamente con los códigos

3. **Validación de códigos**:
   - El otro software escanea el código QR
   - Django valida el UUID y marca como usado en `refrigerio_db`
   - Se registra fecha y hora de uso

## Ventajas
- ✅ No hay duplicación de datos de visitantes
- ✅ Los visitantes se gestionan en un solo lugar (rica_univalle)
- ✅ Control y auditoría de códigos QR separados
- ✅ Los cambios en visitantes se reflejan inmediatamente
- ✅ Sincronización automática

## Modelos

### Visitante (Modelo proxy - solo lectura)
```python
class Visitante(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    identificacion = models.CharField(max_length=50)
    email = models.EmailField()
    
    class Meta:
        managed = False  # Django NO gestiona esta tabla
        db_table = 'visitantes'
```

### CodigoQR (Modelo local - lectura/escritura)
```python
class CodigoQR(models.Model):
    # Información del visitante (copia para auditoría)
    visitante_id = models.IntegerField()
    visitante_nombre = models.CharField(max_length=200)
    visitante_identificacion = models.CharField(max_length=50)
    visitante_email = models.EmailField()
    
    # Datos del código
    tipo_comida = models.CharField(max_length=20)
    codigo = models.UUIDField(unique=True)
    usado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_uso = models.DateTimeField(null=True, blank=True)
```

## Endpoints API

### Listar visitantes
```
GET /api/estudiantes/
GET /api/estudiantes/?activos=true
```

### Generar códigos para un visitante
```
POST /api/estudiantes/{id}/generar_codigos/
```

### Generar códigos masivo
```
POST /api/estudiantes/generar_codigos_masivo/
```

### Ver códigos de un visitante
```
GET /api/estudiantes/{id}/codigos/
```

### Validar código QR
```
POST /api/codigos-qr/validar/
Body: { "codigo": "uuid-del-codigo" }
```

## Configuración

Las credenciales están en `backend/.env`:
```env
DB_NAME=refrigerio_db
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306

EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
```

## Comandos Útiles

### Ver visitantes desde Django shell
```python
from event_management.models import Visitante
visitantes = Visitante.objects.using('rica_univalle').all()
print(f"Total visitantes: {visitantes.count()}")
```

### Ver códigos generados
```python
from event_management.models import CodigoQR
codigos = CodigoQR.objects.all()
print(f"Total códigos: {codigos.count()}")
print(f"Usados: {codigos.filter(usado=True).count()}")
```

### Probar conexión a ambas bases
```bash
python manage.py shell -c "from django.db import connections; connections['default'].ensure_connection(); connections['rica_univalle'].ensure_connection(); print('Ambas BD conectadas OK')"
```

## Notas Importantes

1. **No editar tabla visitantes desde Django**: Esta tabla es gestionada por el otro software
2. **Los códigos QR se guardan localmente**: Para tener control y auditoría
3. **Emails automáticos**: Al generar códigos se envían automáticamente
4. **Sincronización**: Los cambios en visitantes se ven inmediatamente (no hay cache)

## Troubleshooting

### Error: Table visitantes doesn't exist
- Verificar que la BD `rica_univalle` existe
- Verificar credenciales de conexión
- Verificar que la tabla `visitantes` existe en esa BD

### No aparecen visitantes en el frontend
- Verificar conexión a `rica_univalle`
- Revisar logs del servidor Django
- Probar consulta manual desde shell

### Error al generar códigos
- Verificar que `refrigerio_db` existe
- Verificar que las migraciones están aplicadas: `python manage.py migrate`
- Revisar configuración de email si falla el envío
