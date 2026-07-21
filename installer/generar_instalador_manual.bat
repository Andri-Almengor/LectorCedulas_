@echo off
setlocal
cd /d "%~dp0\.."

echo ===============================================
echo  Generador manual del instalador del lector LectorCedulas
echo ===============================================

echo Este BAT genera un instalador generico desde los archivos de template.
echo Para instaladores por cliente y licencia, usa el Dashboard.
echo.

py -m pip install -r requirements.txt
if errorlevel 1 goto error
py -m pip install pyinstaller
if errorlevel 1 goto error

rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
mkdir dist 2>nul
xcopy /E /I /Y template dist\LectorCedulas >nul
cd dist\LectorCedulas
py -m PyInstaller --noconfirm --clean --windowed --onefile --name LectorCedulas --icon assets\icono.ico main.py
if errorlevel 1 goto error
copy /Y dist\LectorCedulas.exe .\LectorCedulas.exe >nul
cd /d "%~dp0\.."

echo.
echo Para generar Setup.exe con licencia por cliente, abre DashboardInstaladores.exe.
pause
exit /b 0

:error
echo.
echo ERROR al generar.
pause
exit /b 1
