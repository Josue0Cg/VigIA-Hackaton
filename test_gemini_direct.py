"""
Test directo del chatbot Gemini sin Django
"""
import sys
import os

# Agregar el directorio al path
sys.path.append('C:/Proyect-Falcon/Proyect_Falcon')

def test_gemini_direct():
    print("🧪 TEST DIRECTO GEMINI")
    print("=" * 40)
    
    try:
        # Importar el chatbot directamente
        from utc_gemini_chatbot import UTCGeminiChatbot
        
        print("✅ Módulo importado correctamente")
        
        # Inicializar
        chatbot = UTCGeminiChatbot()
        print("✅ Chatbot creado")
        
        # Inicializar
        if chatbot.initialize():
            print(f"✅ Chatbot inicializado con {chatbot.utc_context['total_questions']} elementos")
        else:
            print("❌ Error al inicializar chatbot")
            return
        
        # Probar una pregunta
        question = "¿Quién es el rector?"
        print(f"\n🔍 Probando: {question}")
        
        # Primero ver qué contexto encuentra
        processed_question = chatbot.preprocess_question(question)
        print(f"📝 Pregunta procesada: {processed_question}")
        
        relevant_context = chatbot.find_relevant_context(processed_question)
        print(f"📊 Contexto encontrado: {len(relevant_context)} elementos")
        
        for i, item in enumerate(relevant_context, 1):
            print(f"   {i}. P: {item['pregunta'][:50]}...")
            print(f"      R: {item['respuesta'][:100]}...")
        
        result = chatbot.generate_response(question)
        
        if result['success']:
            response = result['response']
            context_count = result.get('relevant_context_count', 0)
            
            print(f"✅ Respuesta generada")
            print(f"📊 Contexto usado: {context_count} elementos")
            print(f"💬 Respuesta: {response}")
            
            # Verificar si es específica de UTC
            utc_keywords = ['sergio', 'alberto', 'guadarrama', 'cortés', 'rector']
            found = [keyword for keyword in utc_keywords if keyword.lower() in response.lower()]
            
            if found:
                print(f"✅ Información específica de UTC encontrada: {found}")
            else:
                print("⚠️ Respuesta parece genérica")
                
        else:
            print(f"❌ Error: {result.get('error', 'Desconocido')}")
            
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_gemini_direct()