# ✅ Sistema Configurado con Doble Base de Datos

## Estado Actual
El sistema ahora está conectado a **dos bases de datos**:
- ✅ `rica_univalle` - BD externa (visitantes)  
- ✅ `refrigerio_db` - BD local (códigos QR)

**Visitantes encontrados**: 1
- Pablo Mora Cristal (111234) - sergiolamoslozano@gmail.com

---

## 🚀 Cómo Iniciar el Sistema

### 1. Iniciar el Backend
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

### 2. Iniciar el Frontend
```powershell
cd frontend
npm run dev
```

### 3. Acceder a la aplicación
- Frontend: http://localhost:5173
- Backend API: http://127.0.0.1:8000/api/

---

## 📋 Flujo de Trabajo

### Ver Visitantes
1. Abre el frontend en http://localhost:5173
2. Verás la lista de visitantes desde `rica_univalle`
3. Los visitantes se muestran en tiempo real (sin duplicar datos)

### Generar Códigos QR
1. Selecciona un visitante de la lista
2. Click en "Generar Códigos"
3. Se crean 3 códigos (DESAYUNO, ALMUERZO, REFRIGERIO)
4. Si el visitante tiene email, se envía automáticamente

### Validar Códigos
1. Escanea el código QR desde la pestaña "Escanear QR"
2. El sistema valida y marca como usado
3. El código solo se puede usar una vez

---

## 🔧 Endpoints API Disponibles

### Listar Visitantes
```
GET http://127.0.0.1:8000/api/estudiantes/
GET http://127.0.0.1:8000/api/estudiantes/?activos=true
```

### Generar Códigos para un Visitante
```
POST http://127.0.0.1:8000/api/estudiantes/{documento}/generar_codigos/
```

### Generar Códigos Masivo
```
POST http://127.0.0.1:8000/api/estudiantes/generar_codigos_masivo/
```

### Ver Códigos de un Visitante
```
GET http://127.0.0.1:8000/api/estudiantes/{documento}/codigos/
```

### Validar Código QR
```
POST http://127.0.0.1:8000/api/codigos-qr/validar/
Body: { "codigo": "uuid-del-codigo" }
```

---

## 🧪 Pruebas

### Probar Conexión a las Bases de Datos
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python test_conexion_bd.py
```

### Probar Envío de Email
```powershell
python test_send_email.py
```

### Ver Visitantes desde Shell
```powershell
python manage.py shell
```
```python
from event_management.models import Visitante
visitantes = Visitante.objects.using('rica_univalle').all()
for v in visitantes:
    print(f"{v.documento}: {v.nombre_completo} - {v.email}")
```

---

## 📊 Estructura de las Bases de Datos

### rica_univalle.visitantes (Externa - Solo Lectura)
```
- documento (PK)
- nombre
- apellido
- tipodocumento
- dependencia
- telefono
- funcionario
- email
```

### refrigerio_db.event_management_codigoqr (Local)
```
- id (PK)
- visitante_id
- visitante_nombre
- visitante_identificacion
- visitante_email
- tipo_comida (DESAYUNO/ALMUERZO/REFRIGERIO)
- codigo (UUID único)
- usado (boolean)
- fecha_creacion
- fecha_uso
```

---

## ⚙️ Configuración de Email

Para que los emails se envíen correctamente:

1. Edita `backend/.env` (o crea el archivo):
```env
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicación
```

2. Genera una contraseña de aplicación de Gmail:
   - Ve a: https://myaccount.google.com/apppasswords
   - Crea una contraseña para "Django Refrigerios"
   - Copia la contraseña (sin espacios)

3. Reinicia el servidor Django

---

## 🔍 Solución de Problemas

### No aparecen visitantes
- Verifica que el servidor Django esté corriendo
- Comprueba conexión a `rica_univalle`: `python test_conexion_bd.py`
- Revisa logs del servidor

### Error al generar códigos
- Verifica que `refrigerio_db` existe
- Aplica migraciones: `python manage.py migrate`
- Revisa que el visitante tenga email válido

### Emails no se envían
- Verifica credenciales en `.env`
- Prueba: `python test_send_email.py`
- Revisa carpeta SPAM del destinatario
- Consulta logs del servidor para ver errores

---

## 📁 Archivos Importantes

- `backend/ARQUITECTURA_DUAL_BD.md` - Documentación de arquitectura
- `backend/test_conexion_bd.py` - Script de prueba de conexiones
- `backend/config/db_router.py` - Router que dirige modelos a sus BD
- `backend/event_management/models.py` - Modelo Visitante (mapea tabla externa)
- `backend/event_management/views_visitantes.py` - ViewSet para visitantes

---

## ✨ Siguiente Paso

**Ahora puedes**: 
1. Reiniciar el servidor Django: `python manage.py runserver`
2. Abrir el frontend y ver el visitante de prueba
3. Generar códigos QR para "Pablo Mora Cristal"
4. El email se enviará a sergiolamoslozano@gmail.com

---

**Fecha**: 21 de octubre de 2025  
**Estado**: ✅ Sistema completamente funcional con arquitectura dual
