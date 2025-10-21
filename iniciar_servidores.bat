@echo off
REM Script para iniciar ambos servidores Django simultáneamente

echo ================================================
echo INICIANDO SERVIDORES DJANGO
echo ================================================
echo.

REM Iniciar servidor RICA (puerto 8000) - ajusta la ruta
echo [1] Iniciando servidor RICA en puerto 8000...
REM start "Django RICA" cmd /k "cd /d C:\ruta\al\software\rica\backend && venv\Scripts\activate && python manage.py runserver 8000"

timeout /t 3 /nobreak > nul

REM Iniciar servidor de Refrigerios (puerto 8001)
echo [2] Iniciando servidor REFRIGERIOS en puerto 8001...
start "Django Refrigerios" cmd /k "cd /d C:\Users\Univalle\Desktop\Prueba Refrigerios\backend && .\venv\Scripts\Activate.ps1 && python manage.py runserver 8001"

echo.
echo ================================================
echo SERVIDORES INICIADOS
echo ================================================
echo.
echo Frontend Refrigerios: http://localhost:5173
echo API RICA:             http://localhost:8000/api/
echo API Refrigerios:      http://localhost:8001/api/
echo.
echo Presiona cualquier tecla para continuar...
pause > nul
