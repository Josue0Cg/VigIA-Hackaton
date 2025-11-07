"""
Test interactivo del chatbot UTC con Gemini
"""

from utc_gemini_chatbot import UTCGeminiChatbot

def test_interactive_questions():
    """Probar preguntas específicas de la UTC"""
    
    print("🤖 INICIANDO TEST INTERACTIVO CHATBOT UTC")
    print("=" * 50)
    
    # Inicializar chatbot
    chatbot = UTCGeminiChatbot()
    if not chatbot.initialize():
        print("❌ Error inicializando chatbot")
        return
    
    # Preguntas específicas de la UTC
    test_questions = [
        "¿Qué carreras ofrece la UTC en logística?",
        "¿Cuándo son los exámenes de ingreso a ingeniería?",
        "¿Quién es el rector de la UTC?",
        "¿Dónde está ubicada la biblioteca?",
        "¿Qué es un TSU?",
        "¿Cuándo es la ceremonia de graduación?",
        "¿Qué programas de licenciatura hay?",
        "¿Cómo contactar a la universidad?"
    ]
    
    successful_responses = 0
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. 👤 Usuario: {question}")
        print("🤖 FALCON:", end=" ")
        
        result = chatbot.generate_response(question)
        
        if result['success']:
            print(result['response'])
            print(f"   📊 Contexto usado: {result['relevant_context_count']} items")
            successful_responses += 1
        else:
            print(f"❌ Error: {result.get('error', 'Unknown')}")
    
    print("\n" + "=" * 50)
    print("📈 RESULTADOS:")
    print(f"   Preguntas procesadas: {len(test_questions)}")
    print(f"   Respuestas exitosas: {successful_responses}")
    print(f"   Tasa de éxito: {(successful_responses/len(test_questions)*100):.1f}%")
    
    # Estadísticas del chatbot
    stats = chatbot.get_session_stats()
    print(f"\n📊 ESTADÍSTICAS DEL CHATBOT:")
    print(f"   Total preguntas: {stats['questions_asked']}")
    print(f"   Respuestas exitosas: {stats['successful_responses']}")
    print(f"   Respuestas fallidas: {stats['failed_responses']}")
    print(f"   Tasa de éxito: {stats['success_rate']:.1f}%")
    print(f"   Items en base de conocimientos: {stats['total_context_items']}")

if __name__ == "__main__":
    test_interactive_questions()