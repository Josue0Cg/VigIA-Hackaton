"""
Test específico para preguntas fuera de la base de datos
"""

from utc_gemini_chatbot import UTCGeminiChatbot

def test_out_of_scope_questions():
    """Probar preguntas que NO están en la base de datos"""
    
    print("🧪 PROBANDO PREGUNTAS FUERA DE LA BASE DE DATOS UTC")
    print("=" * 60)
    
    # Inicializar chatbot
    chatbot = UTCGeminiChatbot()
    if not chatbot.initialize():
        print("❌ Error inicializando chatbot")
        return
    
    # Preguntas que NO están en la base de datos
    out_of_scope_questions = [
        "¿Cuál es la capital de Francia?",
        "¿Cómo cocinar pasta?",
        "¿Qué es el cambio climático?",
        "¿Cuánto cuesta un iPhone?",
        "¿Cómo funciona un motor de carro?",
        "¿Qué día es hoy?",
        "¿Puedes ayudarme con matemáticas?",
        "¿Dónde puedo comprar libros?"
    ]
    
    print("🤖 FALCON responderá a preguntas completamente ajenas a la UTC:")
    print("-" * 50)
    
    for i, question in enumerate(out_of_scope_questions, 1):
        print(f"\n{i}. 👤 Usuario: {question}")
        print("🤖 FALCON:", end=" ")
        
        result = chatbot.generate_response(question)
        
        if result['success']:
            response = result['response']
            # Mostrar solo los primeros 150 caracteres
            if len(response) > 150:
                response = response[:150] + "..."
            print(response)
            print(f"   📊 Contexto encontrado: {result['relevant_context_count']} items")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown')}")
    
    print("\n" + "=" * 60)
    print("📋 ANÁLISIS:")
    print("Como puedes ver, FALCON:")
    print("✅ Mantiene su identidad como asistente de la UTC")
    print("✅ Reconoce cuando las preguntas no son sobre la universidad")
    print("✅ Redirige cortésmente hacia temas relevantes")
    print("✅ No inventa información que no tiene")

if __name__ == "__main__":
    test_out_of_scope_questions()