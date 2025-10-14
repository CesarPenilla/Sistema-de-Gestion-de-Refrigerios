# Frontend - Sistema de Gestión de Refrigerios

Frontend desarrollado con React + Vite para la gestión de refrigerios con códigos QR.

## 🚀 Instalación y Configuración

### 1. Instalar dependencias

```powershell
npm install
```

### 2. Ejecutar servidor de desarrollo

```powershell
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

## 📦 Build para producción

```powershell
npm run build
```

Los archivos de producción se generarán en la carpeta `dist/`

## 🎨 Funcionalidades

### 1. Lista de Estudiantes
- Ver todos los estudiantes registrados
- Eliminar estudiantes
- Ver estado (activo/inactivo)

### 2. Nuevo Estudiante
- Formulario para registrar nuevos estudiantes
- Validación de campos requeridos
- Validación de unicidad de identificación y email

### 3. Generar Códigos QR
- Seleccionar un estudiante
- Generar 3 códigos QR (Desayuno, Almuerzo, Refrigerio)
- Ver códigos QR existentes
- Visualizar imágenes de códigos QR
- Ver estado de uso de cada código

### 4. Escanear Códigos QR
- Escanear códigos QR usando la cámara del dispositivo
- Ingresar códigos manualmente
- Validación en tiempo real
- Marcado automático como "usado"
- Prevención de uso duplicado

## 🛠️ Tecnologías

- **React 18** - Biblioteca de UI
- **Vite** - Build tool y dev server
- **React Router DOM** - Navegación entre páginas
- **Axios** - Cliente HTTP para API
- **HTML5-QRCode** - Librería para escaneo de códigos QR

## 📁 Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/
│   │   ├── EstudiantesList.jsx
│   │   ├── EstudianteForm.jsx
│   │   ├── QRGenerator.jsx
│   │   └── QRScanner.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── index.html
├── vite.config.js
└── package.json
```

## 🔌 Configuración de API

El frontend está configurado para conectarse al backend en `http://localhost:8000/api`

Para cambiar esto, edita la constante `API_URL` en `src/services/api.js`

## 📱 Responsive

La interfaz está optimizada para:
- Desktop
- Tablet
- Móvil

## 🎨 Temas

La aplicación usa un tema oscuro por defecto con:
- Colores personalizados
- Diseño moderno
- Animaciones suaves
- Feedback visual para todas las acciones
