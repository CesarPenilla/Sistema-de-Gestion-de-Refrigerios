# 📧 Configuración de Envío de Emails con Gmail

## 📋 Guía Completa para Configurar Gmail

El sistema ahora envía automáticamente los códigos QR por correo electrónico a los estudiantes cuando se generan. Esta guía te ayudará a configurar Gmail.

---

## 🔐 Paso 1: Crear una Contraseña de Aplicación en Gmail

Google requiere que uses una **Contraseña de Aplicación** en lugar de tu contraseña normal para aplicaciones externas.

### Requisitos Previos:
- ✅ Tener una cuenta de Gmail
- ✅ Tener la verificación en 2 pasos activada

### Pasos para crear la contraseña de aplicación:

1. **Ir a la configuración de tu cuenta de Google:**
   - Ve a: https://myaccount.google.com/

2. **Activar la verificación en 2 pasos** (si no está activada):
   - Ve a **Seguridad** → **Verificación en dos pasos**
   - Sigue las instrucciones para activarla

3. **Crear contraseña de aplicación:**
   - Ve a: https://myaccount.google.com/apppasswords
   - O busca "Contraseñas de aplicaciones" en la configuración de tu cuenta
   - Selecciona **"Correo"** como la aplicación
   - Selecciona **"Otro (nombre personalizado)"** como el dispositivo
   - Escribe: "Django Refrigerios" o el nombre que prefieras
   - Haz clic en **"Generar"**

4. **Copiar la contraseña:**
   - Google te mostrará una contraseña de 16 caracteres
   - **⚠️ Cópiala inmediatamente** (no podrás verla de nuevo)
   - Ejemplo: `abcd efgh ijkl mnop` (sin espacios al usarla)

---

## ⚙️ Paso 2: Configurar Django

### Opción A: Editar settings.py directamente

Abre el archivo `backend/config/settings.py` y busca la sección de EMAIL:

```python
# Email Configuration (Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu_email@gmail.com'  # ← Cambia esto
EMAIL_HOST_PASSWORD = 'abcdefghijklmnop'  # ← Pega tu contraseña de aplicación (sin espacios)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

### Ejemplo Real:
```python
EMAIL_HOST_USER = 'eventos.univalle@gmail.com'
EMAIL_HOST_PASSWORD = 'abcd1234efgh5678'  # Contraseña de aplicación de 16 dígitos
```

---

## 🧪 Paso 3: Probar la Configuración

### Desde el Shell de Django:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py shell
```

Luego ejecuta este código para probar:

```python
from django.core.mail import send_mail

send_mail(
    '🧪 Prueba de Email',
    'Si recibes este mensaje, la configuración está correcta.',
    'sergio.lamos@correounivalle.edu.co',  # Debe coincidir con EMAIL_HOST_USER
    ['sergiolamoslozano@gmail.com'],  # Email donde quieres recibir la prueba
    fail_silently=False,
)
```

Si recibes el email, ¡la configuración está correcta! ✅

---

## 📧 Cómo Funciona el Sistema

### 1. Generación Individual
Cuando generas códigos QR para un estudiante:
1. Se crean 3 códigos QR (Desayuno, Almuerzo, Refrigerio)
2. Se envía automáticamente un email al estudiante
3. El email incluye:
   - Las 3 imágenes QR embebidas
   - Instrucciones de uso
   - Código UUID de cada QR

### 2. Generación Masiva
Cuando usas la generación masiva:
1. Se procesan todos los estudiantes activos sin códigos
2. Se envía un email a cada uno
3. Muestra un resumen:
   - Total de estudiantes procesados
   - Emails enviados exitosamente
   - Emails que fallaron

---

## 📨 Ejemplo de Email que Reciben los Estudiantes

Los estudiantes recibirán un email HTML profesional que incluye:

```
Asunto: 🎫 Tus Códigos QR para el Evento - [Nombre del Estudiante]

Contenido:
- Saludo personalizado
- 3 códigos QR (uno por cada comida) como imágenes
- Instrucciones de uso
- Advertencia de uso único
- Código UUID para cada QR
```

El email se ve así:

- **Header verde** con título del sistema
- **3 secciones** con cada código QR:
  - 📱 DESAYUNO (con imagen QR)
  - 📱 ALMUERZO (con imagen QR)
  - 📱 REFRIGERIO (con imagen QR)
- **Advertencias importantes** en recuadro amarillo
- **Footer** con información del sistema

---

## 🔧 Solución de Problemas

### Error: "SMTPAuthenticationError"
**Causa:** Credenciales incorrectas
**Solución:**
- Verifica que uses la contraseña de aplicación (no tu contraseña normal)
- Asegúrate de copiar la contraseña sin espacios
- Verifica que el email esté correcto

### Error: "SMTPServerDisconnected"
**Causa:** Problemas de conexión
**Solución:**
- Verifica que tengas internet
- Asegúrate de que el puerto 587 no esté bloqueado
- Intenta cambiar `EMAIL_PORT = 587` por `EMAIL_PORT = 465` y `EMAIL_USE_TLS` por `EMAIL_USE_SSL = True`

### Error: "Connection refused"
**Causa:** Firewall o antivirus bloqueando
**Solución:**
- Desactiva temporalmente el firewall
- Agrega una excepción para Python en el antivirus

### Los emails no llegan
**Solución:**
1. Revisa la carpeta de SPAM
2. Verifica que el email del estudiante sea correcto
3. Revisa los logs del backend para ver errores
4. Prueba con el comando de prueba del Paso 3

### Error: "Verificación en 2 pasos no activada"
**Solución:**
- Ve a https://myaccount.google.com/security
- Activa la "Verificación en dos pasos"
- Espera unos minutos y vuelve a intentar crear la contraseña de aplicación

---

## 📊 Ver Logs de Emails

Los emails que fallan se registran en la consola del backend:

```powershell
# Observa la terminal donde corre el backend
python manage.py runserver
```

Verás mensajes como:
```
Error al enviar email: [descripción del error]
```

---

## 🔒 Seguridad

### ⚠️ IMPORTANTE - No subir credenciales a Git

1. **Nunca** subas `settings.py` con tus credenciales reales a repositorios públicos

2. **Mejor práctica:** Usar variables de entorno

Crea un archivo `.env` en la carpeta `backend/`:

```env
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicación
```

Luego en `settings.py`:

```python
import os
from decouple import config  # pip install python-decouple

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
```

3. Agrega `.env` al `.gitignore`:

```gitignore
.env
*.env
```

---

## 📝 Configuración Alternativa (Modo Consola)

Si solo quieres probar sin enviar emails reales:

```python
# En settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Los emails se mostrarán en la consola del backend en lugar de enviarse.

---

## ✅ Checklist de Configuración

- [ ] Cuenta de Gmail lista
- [ ] Verificación en 2 pasos activada
- [ ] Contraseña de aplicación generada
- [ ] `EMAIL_HOST_USER` configurado en settings.py
- [ ] `EMAIL_HOST_PASSWORD` configurado en settings.py
- [ ] Prueba de email exitosa
- [ ] Código QR generado y email recibido
- [ ] Credenciales protegidas (no en Git)

---

## 🎯 Resumen Rápido

```
1. Activa verificación en 2 pasos en Gmail
2. Crea contraseña de aplicación en: https://myaccount.google.com/apppasswords
3. Copia la contraseña (16 caracteres)
4. Edita backend/config/settings.py:
   - EMAIL_HOST_USER = 'tu_email@gmail.com'
   - EMAIL_HOST_PASSWORD = 'contraseña_aplicacion'
5. Reinicia el backend
6. Genera códigos QR → Se envían automáticamente
```

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs del backend
2. Prueba el comando de prueba del Paso 3
3. Verifica que la contraseña de aplicación sea la correcta
4. Consulta: https://support.google.com/accounts/answer/185833

---

**Fecha de implementación:** 14 de octubre de 2025  
**Estado:** ✅ Implementado y funcional
