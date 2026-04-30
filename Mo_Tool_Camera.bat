@echo off
cd /d "%~dp0"
start "" pythonw.exe "%~dp0patch_camera_gui.py"
exit /b
