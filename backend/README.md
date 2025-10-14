# Backend - Sistema de Gestión de Refrigerios

Backend desarrollado con Django y Django REST Framework para la gestión de refrigerios con códigos QR.

## 🚀 Instalación y Configuración

### 1. Crear y activar entorno virtual

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 3. Configurar base de datos

```powershell
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

### 4. Crear superusuario (admin)

```powershell
python manage.py createsuperuser
```

### 5. Ejecutar servidor de desarrollo

```powershell
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

## 📋 Endpoints de la API

### Estudiantes

- **GET** `/api/estudiantes/` - Listar todos los estudiantes
- **POST** `/api/estudiantes/` - Crear nuevo estudiante
- **GET** `/api/estudiantes/{id}/` - Ver detalle de estudiante
- **PUT** `/api/estudiantes/{id}/` - Actualizar estudiante
- **DELETE** `/api/estudiantes/{id}/` - Eliminar estudiante
- **GET** `/api/estudiantes/{id}/con_codigos/` - Ver estudiante con sus códigos QR
- **POST** `/api/estudiantes/{id}/generar_codigos/` - Generar 3 códigos QR para un estudiante

### Códigos QR

- **GET** `/api/codigos-qr/` - Listar todos los códigos QR
- **GET** `/api/codigos-qr/{id}/` - Ver detalle de código QR
- **POST** `/api/codigos-qr/validar/` - Validar y marcar código QR como usado
- **GET** `/api/codigos-qr/{id}/generar_imagen/` - Obtener imagen PNG del código QR
- **GET** `/api/codigos-qr/{id}/generar_base64/` - Obtener código QR en base64
- **GET** `/api/codigos-qr/por_estudiante/?estudiante_id={id}` - Obtener códigos de un estudiante

## 🗄️ Modelos

### Estudiante
```python
- nombre: CharField
- identificacion: CharField (unique)
- email: EmailField (unique)
- activo: BooleanField
- fecha_registro: DateTimeField
```

### CodigoQR
```python
- estudiante: ForeignKey(Estudiante)
- tipo_comida: CharField (DESAYUNO, ALMUERZO, REFRIGERIO)
- codigo: UUIDField (unique)
- usado: BooleanField
- fecha_creacion: DateTimeField
- fecha_uso: DateTimeField
```

## 🔧 Administración

Accede al panel de administración de Django en: `http://localhost:8000/admin`

Usa las credenciales del superusuario que creaste.

## 📦 Dependencias

- Django 5.2.7
- Django REST Framework 3.15.2
- django-cors-headers 4.6.0
- qrcode 8.0
- Pillow 11.1.0

## 🔐 Configuración de CORS

El backend está configurado para aceptar peticiones desde:
- `http://localhost:5173` (Frontend en desarrollo)
- `http://127.0.0.1:5173`

Para modificar esto, edita `CORS_ALLOWED_ORIGINS` en `config/settings.py`
