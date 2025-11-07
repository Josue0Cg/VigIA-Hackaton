"""
Script para verificar modelos disponibles en Gemini
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def check_available_models():
    """Verificar modelos disponibles"""
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ API key no encontrada")
            return
        
        genai.configure(api_key=api_key)
        
        print("🔍 Verificando modelos disponibles...")
        
        # Listar modelos disponibles
        models = genai.list_models()
        
        print("\n📋 MODELOS DISPONIBLES:")
        for model in models:
            print(f"✅ {model.name}")
            if hasattr(model, 'supported_generation_methods'):
                print(f"   Métodos: {model.supported_generation_methods}")
            print()
        
        # Probar modelo específico
        print("🧪 Probando modelo gemini-1.5-flash...")
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("Hola, ¿funcionas?")
            print(f"✅ gemini-1.5-flash: {response.text}")
        except Exception as e:
            print(f"❌ gemini-1.5-flash: {e}")
        
        print("\n🧪 Probando modelo gemini-pro...")
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Hola, ¿funcionas?")
            print(f"✅ gemini-pro: {response.text}")
        except Exception as e:
            print(f"❌ gemini-pro: {e}")
        
        print("\n🧪 Probando modelo gemini-1.5-pro...")
        try:
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content("Hola, ¿funcionas?")
            print(f"✅ gemini-1.5-pro: {response.text}")
        except Exception as e:
            print(f"❌ gemini-1.5-pro: {e}")
            
    except Exception as e:
        print(f"❌ Error verificando modelos: {e}")

if __name__ == "__main__":
    check_available_models()