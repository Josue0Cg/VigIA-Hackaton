#!/usr/bin/env python3
"""
Test de importación de Google Generative AI
"""

print("🔧 Probando importación de Google Generative AI...")

try:
    import google.generativeai as genai
    print("✅ google.generativeai importado correctamente")
    
    # Probar configuración básica
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if api_key and api_key != 'tu_gemini_api_key_aqui':
        genai.configure(api_key=api_key)
        print("✅ API key configurada")
        
        # Probar modelo
        model = genai.GenerativeModel('gemini-2.0-flash')
        print("✅ Modelo Gemini creado correctamente")
        
        # Test simple
        response = model.generate_content("Hola, soy FALCON de la UTC")
        print(f"✅ Respuesta generada: {response.text[:100]}...")
        
    else:
        print("⚠️ API key no encontrada o no configurada")
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    
except Exception as e:
    print(f"❌ Error general: {e}")

print("🔍 Verificando módulos instalados...")
import subprocess
import sys

result = subprocess.run([sys.executable, '-m', 'pip', 'list'], capture_output=True, text=True)
google_packages = [line for line in result.stdout.split('\n') if 'google' in line.lower()]

print("📦 Paquetes Google instalados:")
for pkg in google_packages:
    print(f"  - {pkg}")