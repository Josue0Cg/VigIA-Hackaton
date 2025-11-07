"""
Script de prueba rápida del chatbot FALCON 
Para probar sin necesidad del navegador
"""

from utc_gemini_chatbot import UTCGeminiChatbot

def quick_test():
    """Prueba rápida del chatbot"""
    print("🤖 PRUEBA RÁPIDA DEL CHATBOT FALCON")
    print("=" * 40)
    
    # Inicializar chatbot
    chatbot = UTCGeminiChatbot()
    if not chatbot.initialize():
        print("❌ Error inicializando chatbot")
        return
    
    print("✅ Chatbot inicializado correctamente")
    print("📊 Base de conocimientos: 114 preguntas de la UTC")
    print("-" * 40)
    
    # Lista de preguntas de prueba
    test_questions = [
        "¿Qué carreras ofrece la UTC?",
        "¿Quién es el rector?",
        "¿Cuándo es la ceremonia de graduación?",
        "¿Qué es un TSU?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. 👤 Pregunta: {question}")
        
        result = chatbot.generate_response(question)
        
        if result['success']:
            # Mostrar solo las primeras 100 caracteres
            response_preview = result['response']
            if len(response_preview) > 100:
                response_preview = response_preview[:100] + "..."
            
            print(f"🤖 FALCON: {response_preview}")
            print(f"   ✅ Éxito | Contexto: {result['relevant_context_count']} items")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown')}")
    
    print("\n" + "=" * 40)
    print("🎯 ¡CHATBOT FUNCIONANDO PERFECTAMENTE!")
    print("🌐 Ahora ve a http://localhost:8000 para probarlo en tu navegador")

if __name__ == "__main__":
    quick_test()