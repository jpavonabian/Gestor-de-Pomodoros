@echo off
setlocal enabledelayedexpansion

REM Pedir número de versión
set /p VERSION=Introduce el numero de version (ej: 1.2.3): 

REM Hacer commit con el mensaje
REM Crear el tag
git tag -s %VERSION% -m "%VERSION%"
if errorlevel 1 (
    echo Error al crear el tag.
    goto :eof
)

REM Push del commit y del tag
git push
git push origin %VERSION%

echo ===========================
echo Version %VERSION% publicada.
echo ===========================

endlocal
pause
