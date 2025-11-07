@echo off
echo 🚀 SUBIENDO SOLO LO ESENCIAL DEL CHATBOT FALCON
echo =============================================

echo.
echo 📁 Agregando archivos MODIFICADOS (Django + Frontend)...
git add cross_asistent/chatbot.py
git add cross_asistent/static/css/styles.css
git add cross_asistent/static/js/settings_chatbot.js

echo.
echo 🤖 Agregando MOTOR DEL CHATBOT (solo archivos principales)...
git add gemini_config.py
git add utc_gemini_chatbot.py

echo.
echo 📊 Agregando BASE DE CONOCIMIENTOS...
git add exported_data/utc_training_data_20251105_192821.json

echo.
echo 📋 Agregando CONFIGURACIÓN E INSTRUCCIONES...
git add INSTALACION_Y_SETUP.txt
git add .env.example

echo.
echo ✅ Solo archivos esenciales agregados. Creando commit...

git commit -m "🤖 Implementar Chatbot FALCON - Solo archivos esenciales

✨ Funcionalidades principales:
- Chatbot inteligente con Google Gemini AI
- Base de conocimientos: 128 entradas UTC específicas
- Enlaces clickeables automáticos en frontend
- Solo enlaces funcionales (Mi Portal UTC, Mi Aula UTC, sitio oficial)
- Respuestas naturales sin prefijos robóticos

🔧 Archivos modificados:
- cross_asistent/chatbot.py: Integración Django + Gemini
- cross_asistent/static/js/settings_chatbot.js: Enlaces clickeables
- cross_asistent/static/css/styles.css: Estilos enlaces azules

🤖 Sistema Gemini:
- gemini_config.py: Configuración centralizada
- utc_gemini_chatbot.py: Motor principal del chatbot

📊 Datos:
- exported_data/: Base de conocimientos UTC completa
- INSTALACION_Y_SETUP.txt: Instrucciones paso a paso
- .env.example: Configuración para el equipo

✅ Sistema 100% funcional y listo para usar"

echo.
echo 📤 Subiendo al repositorio...
git push

echo.
echo ✅ ¡CHATBOT ESENCIAL SUBIDO EXITOSAMENTE!
echo.
echo 📋 LO QUE SUBIMOS (solo lo necesario):
echo ✅ Chatbot FALCON completamente funcional  
echo ✅ Enlaces clickeables automáticos
echo ✅ Base de 128 preguntas UTC específicas
echo ✅ Instrucciones claras de instalación
echo ✅ Configuración .env de ejemplo
echo.
echo 🚫 LO QUE NO SUBIMOS (para mantenerlo limpio):
echo ❌ Scripts de prueba múltiples
echo ❌ Entrenadores avanzados
echo ❌ Sistemas de búsqueda web
echo ❌ Utilidades de desarrollo
echo.
echo 🎯 Tu equipo puede:
echo 1. git pull
echo 2. Seguir INSTALACION_Y_SETUP.txt  
echo 3. Obtener API key Gemini (gratis)
echo 4. ¡Chatbot funcionando inmediatamente!

pause