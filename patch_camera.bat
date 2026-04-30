@echo off
setlocal
cd /d "%~dp0"

if "%~1"=="" (
  echo Drag CommonActions.pkg.bytes, Ages folder, or Resources version folder onto this BAT.
  echo.
  echo Optional command line:
  echo   python patch_aov_camera.py "path\to\CommonActions.pkg.bytes" --height 1.5
  echo.
  pause
  exit /b 1
)

python "%~dp0patch_aov_camera.py" "%~1"
echo.
pause
