# 🔄 Ejecución Simultánea de Servidores Django

## 📋 Problema
Necesitas ejecutar dos servidores Django simultáneamente:
- **Software RICA**: Gestiona visitantes en `rica_univalle`
- **Software Refrigerios**: Lee visitantes y genera códigos QR

## ✅ Solución Implementada

### **Arquitectura Actual**

```
┌──────────────────────┐       ┌──────────────────────┐
│   Software RICA      │       │  Software Refrigerios│
│   Puerto 8000        │       │   Puerto 8001        │
│                      │       │                      │
│ • Crear visitantes   │       │ • Leer visitantes    │
│ • Editar visitantes  │       │ • Generar códigos QR │
│ • Eliminar visitantes│       │ • Enviar emails      │
└──────────┬───────────┘       └──────────┬───────────┘
           │                              │
           │     ┌────────────────┐       │
           └────►│  MySQL Server  │◄──────┘
                 │                │
                 │ • rica_univalle │ ← RICA escribe, Refrigerios lee
                 │ • refrigerio_db │ ← Solo Refrigerios escribe
                 └────────────────┘
```

### **¿Por qué Funciona?**

1. **No necesitan comunicarse entre sí** - Ambos comparten las mismas bases de datos
2. **Actualizaciones en tiempo real** - Cuando RICA crea un visitante, Refrigerios lo ve inmediatamente
3. **Puertos diferentes** - No hay conflicto de direcciones

---

## 🚀 Métodos de Inicio

### **Método 1: Script Automático (Recomendado)**

Usa el archivo `iniciar_servidores.bat`:

```powershell
# Ejecutar desde el directorio raíz del proyecto
.\iniciar_servidores.bat
```

Esto abrirá dos ventanas de terminal:
- Terminal 1: Django RICA (puerto 8000) - **debes ajustar la ruta**
- Terminal 2: Django Refrigerios (puerto 8001)

---

### **Método 2: Manual con PowerShell**

#### Terminal 1 - Software RICA
```powershell
cd "C:\ruta\al\software\rica\backend"
.\venv\Scripts\Activate.ps1
python manage.py runserver 8000
```

#### Terminal 2 - Software Refrigerios
```powershell
cd "C:\Users\Univalle\Desktop\Prueba Refrigerios\backend"
.\venv\Scripts\Activate.ps1
python manage.py runserver 8001
```

#### Terminal 3 - Frontend (opcional)
```powershell
cd "C:\Users\Univalle\Desktop\Prueba Refrigerios\frontend"
npm run dev
```

---

### **Método 3: Con Start-Job (PowerShell Background)**

```powershell
# Iniciar servidor RICA en background
$job1 = Start-Job -ScriptBlock {
    Set-Location "C:\ruta\al\software\rica\backend"
    .\venv\Scripts\Activate.ps1
    python manage.py runserver 8000
}

# Iniciar servidor Refrigerios en background
$job2 = Start-Job -ScriptBlock {
    Set-Location "C:\Users\Univalle\Desktop\Prueba Refrigerios\backend"
    .\venv\Scripts\Activate.ps1
    python manage.py runserver 8001
}

# Ver estado
Get-Job

# Detener
Stop-Job $job1, $job2
Remove-Job $job1, $job2
```

---

## 🔧 Configuración Frontend

Si necesitas que tu frontend se comunique con **ambos servidores**:

### `frontend/src/services/api.js`

```javascript
import axios from 'axios';

// Configurar APIs para ambos sistemas
const apiRica = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

const apiRefrigerios = axios.create({
  baseURL: 'http://localhost:8001/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Funciones para sistema de Refrigerios
export const getEstudiantes = () => apiRefrigerios.get('/estudiantes/');
export const generarCodigos = (id) => apiRefrigerios.post(`/estudiantes/${id}/generar_codigos/`);
export const validarCodigo = (codigo) => apiRefrigerios.post('/codigos/validar/', { codigo });

// Funciones para sistema RICA (si necesitas consultarlo directamente)
export const getVisitantesRica = () => apiRica.get('/visitantes/');
export const crearVisitante = (data) => apiRica.post('/visitantes/', data);

export default apiRefrigerios;
```

---

## 📊 Sincronización de Datos

### **¿Cómo se Mantienen Sincronizados?**

**No es necesario sincronizar** - ambos sistemas consultan la misma base de datos:

```sql
-- Cuando RICA crea un visitante:
INSERT INTO rica_univalle.visitantes 
(documento, nombre, apellido, email) 
VALUES ('123456', 'Juan', 'Pérez', 'juan@mail.com');

-- Inmediatamente, Software Refrigerios puede verlo:
SELECT * FROM rica_univalle.visitantes WHERE documento = '123456';
-- ✅ Lo encuentra porque consulta la misma BD
```

### **Flujo de Trabajo Típico:**

1. **Software RICA** (8001): Usuario registra nuevo visitante "María López"
   - Se guarda en `rica_univalle.visitantes`

2. **Software Refrigerios** (8000): Usuario refresca lista de visitantes
   - Consulta `rica_univalle.visitantes`
   - ✅ María López aparece automáticamente

3. **Software Refrigerios**: Usuario genera códigos QR para María
   - Se guardan en `refrigerio_db.event_management_codigoqr`
   - Se envía email con códigos

---

## 🐛 Troubleshooting

### **Error: "Address already in use"**

```
Error: That port is already in use.
```

**Solución**: Otro proceso está usando el puerto. Verifica:

```powershell
# Ver qué está usando el puerto 8000
netstat -ano | findstr :8000

# Matar el proceso (usa el PID del comando anterior)
taskkill /PID <PID> /F
```

### **Error: No se ven los cambios entre sistemas**

**Causa**: Caché de queryset en Django

**Solución**: Ya implementada con `using('rica_univalle')`:

```python
# event_management/views_visitantes.py
def get_queryset(self):
    return Visitante.objects.using('rica_univalle').all()
```

Esto fuerza consultar directamente la BD externa.

### **Error: "Table doesn't exist"**

**Causa**: Migraciones no aplicadas

**Solución**:
```powershell
# Sistema Refrigerios
python manage.py migrate --database=default

# NO migrar rica_univalle (es externa)
# python manage.py migrate --database=rica_univalle  ❌ NO HACER
```

---

## 🎯 URLs de Acceso

Una vez iniciados ambos servidores:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **API RICA** | http://localhost:8000/api/ | Gestión completa visitantes |
| **Admin RICA** | http://localhost:8000/admin/ | Panel administrador RICA |
| **API Refrigerios** | http://localhost:8001/api/ | Visitantes, códigos QR, validación |
| **Admin Refrigerios** | http://localhost:8001/admin/ | Panel administrador |
| **Frontend** | http://localhost:5173 | Interfaz React |

---

## 📝 Endpoints Clave

### **Sistema RICA (8000)** - Ajusta según tu otro software

```bash
# CRUD completo de visitantes
GET    http://localhost:8000/api/visitantes/
POST   http://localhost:8000/api/visitantes/
PUT    http://localhost:8000/api/visitantes/{id}/
DELETE http://localhost:8000/api/visitantes/{id}/
```

### **Sistema Refrigerios (8001)**

```bash
# Listar visitantes desde BD externa
GET http://localhost:8001/api/estudiantes/

# Generar códigos para un visitante
POST http://localhost:8001/api/estudiantes/{documento}/generar_codigos/

# Validar código QR
POST http://localhost:8001/api/codigos/validar/
Body: {"codigo": "DESAYUNO-111234-2025-10-21"}
```

---

## ✅ Checklist de Configuración

- [ ] RICA usa puerto 8000
- [ ] Refrigerios usa puerto 8001
- [ ] Ambos Django configurados para usar MySQL (mismas credenciales)
- [ ] Base de datos `rica_univalle` compartida entre ambos
- [ ] Base de datos `refrigerio_db` solo usada por sistema Refrigerios
- [ ] Modelo `Visitante` en Refrigerios tiene `managed=False`
- [ ] Database router configurado correctamente
- [ ] Frontend configurado con URL correcta de API (http://localhost:8001/api)
- [ ] Script `iniciar_servidores.bat` ajustado con rutas correctas

---

## 🎓 Resumen

**No necesitas sincronización activa** - la arquitectura de base de datos compartida hace que los cambios sean visibles inmediatamente para ambos sistemas. Solo necesitas:

1. ✅ Ejecutar ambos servidores en puertos diferentes
2. ✅ Ambos configurados para la misma BD MySQL
3. ✅ Modelo Visitante en Refrigerios con `managed=False` (ya configurado)

**La sincronización es automática a nivel de base de datos.**
