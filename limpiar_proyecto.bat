@echo off
echo 🧹 LIMPIANDO ARCHIVOS INNECESARIOS DEL PROYECTO
echo ===============================================

echo.
echo 🗑️ Eliminando scripts de prueba múltiples...
del /q test_*.py 2>nul
del /q debug_*.py 2>nul

echo.
echo 🗑️ Eliminando entrenadores y sistemas avanzados innecesarios...
del /q utc_advanced_trainer.py 2>nul
del /q utc_links_trainer.py 2>nul
del /q utc_web_searcher.py 2>nul
del /q gemini_trainer.py 2>nul

echo.
echo 🗑️ Eliminando scripts de mantenimiento...
del /q add_*.py 2>nul
del /q analyze_*.py 2>nul
del /q check_*.py 2>nul
del /q database_manager.py 2>nul
del /q db_stats.py 2>nul
del /q export_database.py 2>nul
del /q update_working_links.py 2>nul
del /q verify_multiple_links.py 2>nul
del /q chat_falcon.py 2>nul

echo.
echo 🗑️ Eliminando archivos de datos innecesarios (conservando solo el principal)...
cd exported_data
del /q backup_*.json 2>nul
del /q categoria_*.json 2>nul
del /q preguntas_usuarios_*.json 2>nul
del /q reporte_*.json 2>nul
del /q utc_database_*.csv 2>nul
del /q utc_database_*.json 2>nul
del /q utc_enhanced_*.json 2>nul
del /q utc_preguntas_*.txt 2>nul
del /q utc_training_*.csv 2>nul
del /q advanced_prompts.json 2>nul
del /q conversation_logs.json 2>nul
del /q link_detection_rules.json 2>nul
del /q smart_link_patterns.json 2>nul
rmdir /s /q backups 2>nul
cd ..

echo.
echo 🗑️ Eliminando guías y documentos extensos innecesarios...
del /q GUIA_CHATBOT_FALCON_FINAL.md 2>nul

echo.
echo 🗑️ Eliminando scripts de subida antiguos...
del /q subir_cambios.bat 2>nul

echo.
echo ✅ LIMPIEZA COMPLETADA
echo.
echo 📊 ARCHIVOS CONSERVADOS (solo lo esencial):
echo ✅ gemini_config.py - Configuración chatbot
echo ✅ utc_gemini_chatbot.py - Motor principal
echo ✅ exported_data/utc_training_data_20251105_192821.json - Base de conocimientos
echo ✅ INSTALACION_Y_SETUP.txt - Instrucciones
echo ✅ .env.example - Configuración ejemplo
echo ✅ quick_check.py - Verificación rápida
echo ✅ quick_test_falcon.py - Prueba básica
echo ✅ start_server.bat - Utilidad servidor
echo ✅ subir_esencial.bat - Script de subida
echo.
echo 🧹 ARCHIVOS ELIMINADOS:
echo ❌ 15+ scripts de prueba
echo ❌ Entrenadores avanzados
echo ❌ Sistemas de búsqueda web
echo ❌ 20+ archivos de backup y datos duplicados
echo ❌ Guías extensas
echo ❌ Scripts de mantenimiento
echo.
echo 💾 Espacio liberado significativamente
echo 🎯 Solo archivos útiles para el equipo

pause