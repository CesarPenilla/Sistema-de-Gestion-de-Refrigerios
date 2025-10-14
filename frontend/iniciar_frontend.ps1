# Script para iniciar el Frontend React
# Ejecutar este archivo haciendo doble clic o desde PowerShell

Write-Host "🚀 Iniciando Frontend React + Vite..." -ForegroundColor Green
Write-Host ""

# Navegar a la carpeta frontend
Set-Location -Path $PSScriptRoot

# Verificar si node_modules existe
if (!(Test-Path "node_modules")) {
    Write-Host "📦 Instalando dependencias..." -ForegroundColor Yellow
    npm install
}

# Iniciar servidor de desarrollo
Write-Host "🌐 Iniciando servidor Vite en http://localhost:5173" -ForegroundColor Cyan
Write-Host "⚠️  Presiona CTRL+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

npm run dev
