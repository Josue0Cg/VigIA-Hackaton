"""
Script de debug para verificar que Django puede acceder al chatbot Gemini
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cross_project.settings')

# Agregar el directorio del proyecto al path
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.append(project_dir)

django.setup()

def test_django_integration():
    """Probar la integración con Django"""
    print("🔍 DEPURANDO INTEGRACIÓN DJANGO + GEMINI")
    print("=" * 50)
    
    # Test 1: Verificar importación
    print("1️⃣ Verificando importación del chatbot...")
    try:
        from utc_gemini_chatbot import UTCGeminiChatbot
        print("✅ utc_gemini_chatbot importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando utc_gemini_chatbot: {e}")
        return False
    
    # Test 2: Verificar inicialización
    print("\n2️⃣ Verificando inicialización del chatbot...")
    try:
        chatbot = UTCGeminiChatbot()
        if chatbot.initialize():
            print("✅ Chatbot inicializado correctamente")
            print(f"📊 Base de conocimientos: {chatbot.utc_context['total_questions']} preguntas")
        else:
            print("❌ Error inicializando chatbot")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 3: Verificar respuesta
    print("\n3️⃣ Verificando respuesta de prueba...")
    try:
        result = chatbot.generate_response("¿Quién es el rector?")
        if result['success']:
            print("✅ Respuesta generada correctamente")
            print(f"📝 Respuesta: {result['response'][:100]}...")
            print(f"📊 Contexto: {result['relevant_context_count']} items")
        else:
            print(f"❌ Error en respuesta: {result.get('error', 'Unknown')}")
            return False
    except Exception as e:
        print(f"❌ Error generando respuesta: {e}")
        return False
    
    # Test 4: Verificar que Django puede usar el chatbot
    print("\n4️⃣ Verificando integración con Django...")
    try:
        from cross_asistent.chatbot import get_gemini_chatbot
        django_chatbot = get_gemini_chatbot()
        if django_chatbot:
            print("✅ Django puede acceder al chatbot")
        else:
            print("❌ Django no puede acceder al chatbot")
            return False
    except Exception as e:
        print(f"❌ Error en integración Django: {e}")
        return False
    
    print("\n✅ TODOS LOS TESTS PASARON")
    print("🎯 El chatbot debería funcionar correctamente en Django")
    return True

if __name__ == "__main__":
    test_django_integration()