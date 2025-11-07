"""
Test del sistema híbrido: Base de datos + Búsqueda Web
"""
import sys
import os

# Agregar el directorio al path
sys.path.append('C:/Proyect-Falcon/Proyect_Falcon')

def test_hybrid_system():
    print("🧪 TEST SISTEMA HÍBRIDO (BD + WEB)")
    print("=" * 50)
    
    try:
        from utc_gemini_chatbot import UTCGeminiChatbot
        
        # Inicializar chatbot
        chatbot = UTCGeminiChatbot()
        
        if not chatbot.initialize():
            print("❌ Error al inicializar chatbot")
            return
        
        print(f"✅ Chatbot inicializado con {chatbot.utc_context['total_questions']} elementos")
        
        if chatbot.web_searcher:
            print("🌐 Sistema de búsqueda web activado")
        else:
            print("⚠️ Sistema de búsqueda web no disponible")
        
        # Preguntas de prueba para diferentes escenarios
        test_questions = [
            # Información que SÍ está en la BD
            "¿Quién es el rector?",
            
            # Información que probablemente NO está completa en la BD
            "¿Cuánto cuesta estudiar en la UTC?",
            "¿Cuál es la dirección exacta de la universidad?",
            "¿Cuál es el teléfono de contacto?",
            "¿Cuáles son los horarios de atención?",
            
            # Pregunta general
            "¿Qué es la inteligencia artificial?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n{i}. 👤 Pregunta: {question}")
            print("-" * 40)
            
            try:
                result = chatbot.generate_response(question)
                
                if result['success']:
                    response = result['response']
                    context_count = result.get('relevant_context_count', 0)
                    web_enhanced = result.get('web_enhanced', False)
                    
                    print(f"📊 Contexto BD: {context_count} items")
                    print(f"🌐 Búsqueda web: {'✅ Sí' if web_enhanced else '❌ No'}")
                    print(f"📝 Respuesta ({len(response)} chars):")
                    
                    # Mostrar respuesta dividida si es muy larga
                    if len(response) > 300:
                        print(f"   {response[:300]}...")
                        if "📍 INFORMACIÓN ADICIONAL" in response:
                            web_part = response.split("📍 INFORMACIÓN ADICIONAL")[1][:200]
                            print(f"   \n🌐 Info web: {web_part}...")
                    else:
                        print(f"   {response}")
                    
                    # Análisis de calidad
                    quality_indicators = {
                        'specific_info': any(word in response.lower() for word in [
                            'sergio alberto', 'guadarrama', 'rector', 'utc', 'coahuila'
                        ]),
                        'detailed': len(response) > 150,
                        'web_enriched': web_enhanced,
                        'natural_tone': not response.startswith(('🤖', 'FALCON:'))
                    }
                    
                    quality_score = sum(quality_indicators.values())
                    print(f"🎯 Calidad: {quality_score}/4 {'✅' if quality_score >= 3 else '⚠️'}")
                    
                else:
                    print(f"❌ Error: {result.get('error', 'Unknown')}")
                    
            except Exception as e:
                print(f"❌ Excepción: {e}")
        
        # Mostrar estadísticas de la sesión
        stats = chatbot.session_stats
        print(f"\n📊 ESTADÍSTICAS DE LA SESIÓN:")
        print(f"  Preguntas procesadas: {stats['questions_asked']}")
        print(f"  Respuestas exitosas: {stats['successful_responses']}")
        print(f"  Búsquedas web realizadas: {stats['web_searches_used']}")
        print(f"  Ratio web/total: {stats['web_searches_used']/stats['questions_asked']*100:.1f}%")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Asegúrate de que todas las dependencias estén instaladas")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_hybrid_system()