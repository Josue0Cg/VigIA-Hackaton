"""
Chat interactivo con FALCON por terminal
Perfecto para hacer pruebas rápidas y extensas
"""

from utc_gemini_chatbot import UTCGeminiChatbot

def interactive_chat():
    """Chat interactivo con FALCON"""
    print("🤖 CHAT INTERACTIVO CON FALCON")
    print("🎓 Asistente Virtual de la Universidad Tecnológica de Coahuila")
    print("=" * 60)
    
    # Inicializar chatbot
    chatbot = UTCGeminiChatbot()
    if not chatbot.initialize():
        print("❌ Error inicializando chatbot")
        print("Verifica tu conexión a internet y API key de Gemini")
        return
    
    print("✅ FALCON inicializado correctamente")
    print(f"📊 Base de conocimientos: {chatbot.utc_context['total_questions']} preguntas")
    print("\n💡 COMANDOS ESPECIALES:")
    print("   'salir' - Terminar chat")
    print("   'stats' - Ver estadísticas")
    print("   'help' - Ayuda")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\n👤 Tú: ").strip()
            
            if user_input.lower() in ['salir', 'exit', 'quit', 'bye']:
                print("\n🤖 FALCON: ¡Hasta luego! Espero haberte ayudado con información sobre la UTC. 😊")
                break
            
            if user_input.lower() == 'stats':
                stats = chatbot.get_session_stats()
                print(f"\n📊 ESTADÍSTICAS DE LA SESIÓN:")
                print(f"   Preguntas realizadas: {stats['questions_asked']}")
                print(f"   Respuestas exitosas: {stats['successful_responses']}")
                print(f"   Tasa de éxito: {stats['success_rate']:.1f}%")
                print(f"   Duración: {stats['session_duration_seconds']:.1f} segundos")
                continue
            
            if user_input.lower() == 'help':
                print("\n🆘 AYUDA - EJEMPLOS DE PREGUNTAS:")
                print("   • ¿Qué carreras ofrece la UTC?")
                print("   • ¿Quién es el rector?")
                print("   • ¿Cuándo son los exámenes de ingreso?")
                print("   • ¿Qué es un TSU?")
                print("   • ¿Cuándo es la ceremonia de graduación?")
                print("   • ¿Dónde está la biblioteca?")
                continue
            
            if not user_input:
                print("🤖 FALCON: Por favor, escribe tu pregunta sobre la UTC 😊")
                continue
            
            print("🤖 FALCON: ", end="")
            
            # Generar respuesta
            result = chatbot.generate_response(user_input)
            
            if result['success']:
                print(result['response'])
                print(f"   📊 Contexto usado: {result['relevant_context_count']} items de la base de conocimientos")
            else:
                print("Lo siento, ocurrió un error técnico. Por favor, intenta de nuevo.")
                print(f"   ⚠️ Error: {result.get('error', 'Unknown')}")
        
        except KeyboardInterrupt:
            print("\n\n🤖 FALCON: ¡Hasta luego! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
    
    # Mostrar estadísticas finales
    try:
        final_stats = chatbot.get_session_stats()
        print(f"\n📈 RESUMEN FINAL:")
        print(f"   Total preguntas: {final_stats['questions_asked']}")
        print(f"   Respuestas exitosas: {final_stats['successful_responses']}")
        print(f"   Tasa de éxito: {final_stats['success_rate']:.1f}%")
        print(f"   Duración total: {final_stats['session_duration_seconds']:.1f} segundos")
        print("\n🌐 ¡También puedes probar FALCON en http://localhost:8000!")
    except:
        pass

if __name__ == "__main__":
    interactive_chat()