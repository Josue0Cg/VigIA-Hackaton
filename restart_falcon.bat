@echo off
cd /d "C:\Proyect-Falcon\Proyect_Falcon"
call .\.venv\Scripts\activate.bat
echo 🚀 REINICIANDO SERVIDOR FALCON CON GEMINI
echo =============================================
python manage.py runserver
pause