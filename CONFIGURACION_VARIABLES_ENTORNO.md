# 🔐 Configuración de Variables de Entorno

Este proyecto utiliza variables de entorno para proteger datos sensibles como contraseñas de bases de datos y credenciales de email.

## 📋 Instalación Inicial

### 1. Copiar el archivo de ejemplo

```powershell
cd backend
cp .env.example .env
```

### 2. Editar el archivo `.env`

Abre el archivo `.env` y configura las siguientes variables:

```env
# Django Configuration
SECRET_KEY=tu-secret-key-aqui                    # Genera una nueva con Django
DEBUG=True                                        # False en producción
ALLOWED_HOSTS=localhost,127.0.0.1                # Agregar dominio en producción

# Database Configuration - Default (refrigerio_db)
DB_NAME=refrigerio_db                            # Nombre de tu BD local
DB_USER=root                                      # Tu usuario MySQL
DB_PASSWORD=tu-contraseña-mysql                  # ⚠️ TU CONTRASEÑA MYSQL
DB_HOST=localhost                                 # Servidor de BD
DB_PORT=3306                                      # Puerto MySQL

# Database Configuration - RICA (rica_univalle)
DB_RICA_NAME=rica_univalle                       # Nombre BD externa
DB_RICA_USER=root                                # Usuario BD externa
DB_RICA_PASSWORD=tu-contraseña-mysql            # ⚠️ CONTRASEÑA BD EXTERNA
DB_RICA_HOST=localhost                           # Servidor BD externa
DB_RICA_PORT=3306                                # Puerto BD externa

# Email Configuration (Gmail)
EMAIL_HOST_USER=tu-email@gmail.com              # ⚠️ TU EMAIL GMAIL
EMAIL_HOST_PASSWORD=tu-contraseña-app-gmail     # ⚠️ CONTRASEÑA DE APLICACIÓN
DEFAULT_FROM_EMAIL=tu-email@gmail.com           # Email remitente
```

---

## 🔑 Obtener Contraseña de Aplicación de Gmail

Para enviar emails desde Gmail, necesitas una **Contraseña de Aplicación** (no tu contraseña normal):

### Pasos:

1. **Ir a tu cuenta de Google**: https://myaccount.google.com/
2. **Seguridad** → **Verificación en 2 pasos** (debes activarla primero)
3. **Contraseñas de aplicaciones**: https://myaccount.google.com/apppasswords
4. **Seleccionar app**: "Correo"
5. **Seleccionar dispositivo**: "Windows/Mac/Linux"
6. **Generar** → Copiar la contraseña de 16 caracteres
7. **Pegar en `.env`** en `EMAIL_HOST_PASSWORD` (sin espacios)

**Ejemplo:**
```env
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop    # ❌ MAL (con espacios)
EMAIL_HOST_PASSWORD=abcdefghijklmnop       # ✅ BIEN (sin espacios)
```

---

## 🔒 Generar una Nueva SECRET_KEY de Django

Si necesitas generar una nueva `SECRET_KEY`:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y pégalo en `.env`:

```env
SECRET_KEY=nueva-secret-key-generada-aqui
```

---

## 📂 Estructura de Archivos

```
backend/
├── .env                    # ⚠️ NUNCA SUBIR A GIT (tiene contraseñas)
├── .env.example            # ✅ Plantilla sin datos sensibles
├── .gitignore              # Asegura que .env no se suba
└── config/
    └── settings.py         # Lee variables desde .env
```

---

## ✅ Verificar Configuración

Para verificar que las variables se cargan correctamente:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py shell
```

Dentro del shell de Django:

```python
from decouple import config

# Verificar variables
print("DB Password:", config('DB_PASSWORD'))
print("Email User:", config('EMAIL_HOST_USER'))
print("Debug Mode:", config('DEBUG', cast=bool))
```

---

## 🚨 Seguridad

### ✅ DO (Hacer):
- ✅ Mantener `.env` en `.gitignore`
- ✅ Usar `.env.example` para documentar variables requeridas
- ✅ Nunca commitear contraseñas en el código
- ✅ Usar contraseñas de aplicación para Gmail (no contraseña normal)
- ✅ Cambiar `DEBUG=False` en producción
- ✅ Generar nueva `SECRET_KEY` en producción

### ❌ DON'T (No hacer):
- ❌ Subir `.env` a GitHub/GitLab
- ❌ Hardcodear contraseñas en `settings.py`
- ❌ Compartir `.env` por email/chat
- ❌ Usar la misma `SECRET_KEY` en desarrollo y producción
- ❌ Dejar `DEBUG=True` en producción

---

## 🔄 Cambiar Contraseñas

Si cambias contraseñas de BD o email:

1. **Editar `.env`** con las nuevas credenciales
2. **NO es necesario reiniciar** - Django recarga automáticamente
3. **Verificar** que funcione haciendo una prueba

---

## 📝 Variables Disponibles

| Variable | Descripción | Requerida | Default |
|----------|-------------|-----------|---------|
| `SECRET_KEY` | Clave secreta Django | ❌ | Auto-generada |
| `DEBUG` | Modo debug | ❌ | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos | ❌ | `localhost,127.0.0.1` |
| `DB_NAME` | Nombre BD local | ❌ | `refrigerio_db` |
| `DB_USER` | Usuario BD local | ❌ | `root` |
| `DB_PASSWORD` | Contraseña BD local | ✅ | - |
| `DB_HOST` | Host BD local | ❌ | `localhost` |
| `DB_PORT` | Puerto BD local | ❌ | `3306` |
| `DB_RICA_NAME` | Nombre BD RICA | ❌ | `rica_univalle` |
| `DB_RICA_USER` | Usuario BD RICA | ❌ | `root` |
| `DB_RICA_PASSWORD` | Contraseña BD RICA | ✅ | - |
| `DB_RICA_HOST` | Host BD RICA | ❌ | `localhost` |
| `DB_RICA_PORT` | Puerto BD RICA | ❌ | `3306` |
| `EMAIL_HOST_USER` | Email Gmail | ✅ | - |
| `EMAIL_HOST_PASSWORD` | Contraseña app Gmail | ✅ | - |
| `DEFAULT_FROM_EMAIL` | Email remitente | ❌ | Mismo que `EMAIL_HOST_USER` |

---

## 🆘 Solución de Problemas

### Error: "No module named 'decouple'"

```powershell
pip install python-decouple
```

### Error: "Access denied for user 'root'@'localhost'"

- Verifica que `DB_PASSWORD` y `DB_RICA_PASSWORD` sean correctas
- Asegúrate de que MySQL esté corriendo

### Error: "SMTPAuthenticationError"

- Verifica que `EMAIL_HOST_PASSWORD` sea una **contraseña de aplicación**, no tu contraseña normal
- Elimina espacios de la contraseña
- Asegúrate de tener activada la verificación en 2 pasos en Google

### El archivo `.env` no se carga

- Verifica que esté en `backend/.env` (mismo nivel que `manage.py`)
- Asegúrate de que no tenga espacios extras o caracteres raros
- Reinicia el servidor Django

---

## 📚 Recursos

- **python-decouple**: https://github.com/HBNetwork/python-decouple
- **Contraseñas de aplicación Gmail**: https://support.google.com/accounts/answer/185833
- **Django Settings**: https://docs.djangoproject.com/en/5.2/topics/settings/
