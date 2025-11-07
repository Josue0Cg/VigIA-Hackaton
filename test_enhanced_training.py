"""
Test de las mejoras de entrenamiento del chatbot UTC
"""
import sys
import os

# Agregar el directorio al path
sys.path.append('C:/Proyect-Falcon/Proyect_Falcon')

def test_enhanced_training():
    print("🧪 TEST DE MEJORAS DE ENTRENAMIENTO")
    print("=" * 50)
    
    try:
        from utc_gemini_chatbot import UTCGeminiChatbot
        
        # Inicializar chatbot con datos mejorados
        chatbot = UTCGeminiChatbot()
        
        if not chatbot.initialize():
            print("❌ Error al inicializar chatbot")
            return
        
        print(f"✅ Chatbot inicializado con {chatbot.utc_context['total_questions']} elementos")
        
        if chatbot.utc_context.get('enhanced_data', False):
            print("🚀 Usando datos de entrenamiento mejorados")
        else:
            print("⚠️ Usando datos originales")
        
        # Preguntas de prueba para verificar mejoras
        test_questions = [
            "¿Quién es el rector?",
            "Información del rector",
            "¿Cómo se llama el director de la UTC?",
            "¿Qué carreras hay?",
            "¿Cuáles son los programas académicos?",
            "¿Dónde está la universidad?",
            "¿Cuánto cuesta estudiar?",
            "¿Cuánto es 5 + 5?",  # Pregunta general
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n{i}. 👤 Pregunta: {question}")
            
            try:
                result = chatbot.generate_response(question)
                
                if result['success']:
                    response = result['response']
                    context_count = result.get('relevant_context_count', 0)
                    
                    print(f"   📊 Contexto: {context_count} items")
                    print(f"   📝 Respuesta: {response[:120]}...")
                    
                    # Verificar calidad de respuesta
                    quality_indicators = {
                        'utc_specific': any(word in response.lower() for word in [
                            'universidad tecnológica', 'coahuila', 'sergio alberto', 
                            'guadarrama', 'rector', 'utc'
                        ]),
                        'detailed': len(response) > 100,
                        'no_prefixes': not response.startswith(('🤖', 'FALCON:')),
                        'natural_tone': not any(phrase in response for phrase in [
                            'no tengo información', 'no cuento con', 'lamento no poder'
                        ]) if context_count > 0 else True
                    }
                    
                    quality_score = sum(quality_indicators.values())
                    print(f"   🎯 Calidad: {quality_score}/4 {'✅' if quality_score >= 3 else '⚠️'}")
                    
                    if not quality_indicators['utc_specific'] and any(word in question.lower() for word in ['rector', 'carrera', 'universidad']):
                        print("   ⚠️ Falta información específica de UTC")
                    
                    if not quality_indicators['no_prefixes']:
                        print("   ⚠️ Contiene prefijos innecesarios")
                    
                else:
                    print(f"   ❌ Error: {result.get('error', 'Unknown')}")
                    
            except Exception as e:
                print(f"   ❌ Excepción: {e}")
        
        print("\n" + "=" * 50)
        print("🎯 Test de entrenamiento completado")
        
        # Mostrar estadísticas de la base de datos
        categories = chatbot.utc_context.get('categories', {})
        print(f"\n📊 Estadísticas de la base de conocimientos:")
        for categoria, items in categories.items():
            enhanced_count = sum(1 for item in items if item.get('enhanced', False))
            print(f"  {categoria}: {len(items)} items ({enhanced_count} mejorados)")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_enhanced_training()