"""
Test rápido de las mejoras implementadas
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cross_project.settings')
django.setup()

# Importar módulos después de configurar Django
from cross_asistent.chatbot import get_gemini_chatbot

def test_improved_chatbot():
    """Probar las mejoras del chatbot"""
    
    print("🧪 PROBANDO CHATBOT MEJORADO")
    print("=" * 40)
    
    # Inicializar chatbot
    chatbot = get_gemini_chatbot()
    
    if not chatbot:
        print("❌ No se pudo inicializar el chatbot")
        return
    
    print("✅ Chatbot inicializado correctamente")
    
    # Preguntas de prueba
    test_questions = [
        "¿Quién es el rector?",
        "¿Qué carreras tiene la UTC?", 
        "¿Cuánto es 2 + 2?",  # Pregunta general
        "¿Qué es la fotosíntesis?",  # Pregunta general
        "¿Cuándo es la ceremonia de graduación?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. 👤 Pregunta: {question}")
        
        try:
            result = chatbot.generate_response(question)
            
            if result['success']:
                response = result['response']
                context_count = result.get('relevant_context_count', 0)
                
                print(f"   📊 Contexto UTC: {context_count} items")
                print(f"   🤖 Respuesta: {response[:150]}...")
                
                # Verificar mejoras
                if response.startswith("🤖 FALCON:"):
                    print("   ⚠️ Aún tiene prefijo 'FALCON:'")
                else:
                    print("   ✅ Sin prefijo innecesario")
                
                if "🤖" in response:
                    print("   ⚠️ Aún tiene emoji de robot")
                else:
                    print("   ✅ Sin emoji de robot")
                    
            else:
                print(f"   ❌ Error: {result.get('error', 'Unknown')}")
                
        except Exception as e:
            print(f"   ❌ Excepción: {e}")
    
    print("\n" + "=" * 40)
    print("🎯 Prueba completada")

if __name__ == "__main__":
    test_improved_chatbot()