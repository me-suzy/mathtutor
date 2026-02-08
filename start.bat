@echo off
chcp 65001 >nul
title Tutor Matematic Vocal

echo.
echo ======================================
echo    TUTOR MATEMATIC VOCAL
echo ======================================
echo.

rem MODIFICA AICI - pune API key-ul tau Anthropic
set "ANTHROPIC_API_KEY=YOUR-API-KEY"

if "%ANTHROPIC_API_KEY%"=="sk-ant-api03-PUNE-AICI-KEY-UL-TAU" (
    echo ATENTIE: Deschide start.bat cu Notepad si pune API key-ul tau!
    echo.
    echo    Linia: set "ANTHROPIC_API_KEY=sk-ant-api03-..."
    echo.
    echo    Obtine key de pe: https://console.anthropic.com/settings/keys
    echo.
    pause
    exit /b
)

echo Pornesc serverul... (asteapta cateva secunde)
echo.
echo    Ctrl+C pentru a opri
echo.

start /b cmd /c "timeout /t 15 /nobreak >nul & start http://localhost:5000"
python app.py

pause
