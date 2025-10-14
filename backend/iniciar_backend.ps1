# Script para iniciar el Backend de Django
# Ejecutar este archivo haciendo doble clic o desde PowerShell

Write-Host "🚀 Iniciando Backend Django..." -ForegroundColor Green
Write-Host ""

# Navegar a la carpeta backend
Set-Location -Path $PSScriptRoot

# Activar entorno virtual
Write-Host "📦 Activando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Iniciar servidor Django
Write-Host "🌐 Iniciando servidor Django en http://localhost:8000" -ForegroundColor Cyan
Write-Host "⚠️  Presiona CTRL+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver
