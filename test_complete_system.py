"""
Test del Sistema Completo: BD + Web + Enlaces Oficiales
"""
import sys
import os

# Agregar el directorio al path
sys.path.append('C:/Proyect-Falcon/Proyect_Falcon')

def test_complete_system():
    print("🧪 TEST SISTEMA COMPLETO (BD + WEB + ENLACES)")
    print("=" * 60)
    
    try:
        from utc_gemini_chatbot import UTCGeminiChatbot
        
        # Inicializar chatbot
        chatbot = UTCGeminiChatbot()
        
        if not chatbot.initialize():
            print("❌ Error al inicializar chatbot")
            return
        
        print(f"✅ Chatbot inicializado con {chatbot.utc_context['total_questions']} elementos")
        print(f"📊 Versión de datos: {chatbot.utc_context.get('version', 'desconocida')}")
        
        if chatbot.utc_context.get('has_official_links', False):
            print("🔗 Sistema de enlaces oficiales activado")
        
        if chatbot.web_searcher:
            print("🌐 Sistema de búsqueda web activado")
        
        if chatbot.links_system and chatbot.links_system.get('enabled', False):
            print("📎 Sistema de detección de enlaces activado")
        
        # Preguntas específicas para probar cada sistema
        test_scenarios = [
            {
                "category": "BD + Enlaces",
                "question": "¿Quién es el rector?",
                "expected": ["sergio alberto", "guadarrama", "rector"]
            },
            {
                "category": "Enlaces Costos",
                "question": "¿Cuánto cuesta estudiar en la UTC?",
                "expected": ["costo", "utc.edu.mx", "enlaces"]
            },
            {
                "category": "Enlaces Ubicación",
                "question": "¿Dónde está la universidad?",
                "expected": ["contacto", "https://", "ubicación"]
            },
            {
                "category": "Enlaces Carreras",
                "question": "¿Qué carreras ofrece la UTC?",
                "expected": ["carrera", "programa", "https://"]
            },
            {
                "category": "Enlaces Trámites",
                "question": "¿Cómo genero una constancia?",
                "expected": ["mi portal", "trámite", "https://mi.utc.edu.mx"]
            },
            {
                "category": "General",
                "question": "¿Qué es la inteligencia artificial?",
                "expected": ["inteligencia artificial", "ia"]
            }
        ]
        
        results = []
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n{i}. 🎯 {scenario['category']}: {scenario['question']}")
            print("-" * 60)
            
            try:
                result = chatbot.generate_response(scenario['question'])
                
                if result['success']:
                    response = result['response']
                    context_count = result.get('relevant_context_count', 0)
                    web_enhanced = result.get('web_enhanced', False)
                    links_added = result.get('links_added', False)
                    
                    print(f"📊 Contexto BD: {context_count} items")
                    print(f"🌐 Búsqueda web: {'✅' if web_enhanced else '❌'}")
                    print(f"🔗 Enlaces agregados: {'✅' if links_added else '❌'}")
                    print(f"📝 Longitud respuesta: {len(response)} chars")
                    
                    # Verificar contenido esperado
                    response_lower = response.lower()
                    found_expected = [exp for exp in scenario['expected'] if exp.lower() in response_lower]
                    
                    # Verificar si tiene enlaces oficiales
                    has_official_links = any(link in response for link in [
                        'https://utc.edu.mx', 'https://mi.utc.edu.mx', 'utc.edu.mx'
                    ])
                    
                    # Calcular puntuación
                    score = 0
                    if context_count > 0: score += 1
                    if len(found_expected) > 0: score += 1
                    if has_official_links and any(word in scenario['question'].lower() for word in ['costo', 'donde', 'carrera', 'tramite', 'constancia']): score += 1
                    if len(response) > 200: score += 1
                    
                    quality = "🟢 Excelente" if score >= 3 else "🟡 Bueno" if score >= 2 else "🔴 Mejorable"
                    
                    print(f"🎯 Contenido encontrado: {found_expected}")
                    print(f"🔗 Enlaces oficiales: {'✅' if has_official_links else '❌'}")
                    print(f"📈 Calidad: {score}/4 {quality}")
                    
                    # Mostrar preview de la respuesta
                    if len(response) > 200:
                        print(f"📖 Preview: {response[:200]}...")
                        if has_official_links:
                            # Mostrar parte de los enlaces
                            if "📍" in response:
                                links_part = response.split("📍")[1][:150]
                                print(f"🔗 Enlaces: ...{links_part}...")
                    else:
                        print(f"📖 Respuesta: {response}")
                    
                    results.append({
                        'scenario': scenario['category'],
                        'question': scenario['question'],
                        'score': score,
                        'has_links': has_official_links,
                        'web_enhanced': web_enhanced,
                        'context_count': context_count
                    })
                    
                else:
                    print(f"❌ Error: {result.get('error', 'Unknown')}")
                    results.append({
                        'scenario': scenario['category'],
                        'question': scenario['question'],
                        'score': 0,
                        'error': True
                    })
                    
            except Exception as e:
                print(f"❌ Excepción: {e}")
                results.append({
                    'scenario': scenario['category'],
                    'question': scenario['question'],
                    'score': 0,
                    'error': True
                })
        
        # Mostrar resumen final
        print(f"\n📊 RESUMEN FINAL DEL SISTEMA COMPLETO")
        print("=" * 60)
        
        total_score = sum(r.get('score', 0) for r in results if not r.get('error', False))
        max_score = len([r for r in results if not r.get('error', False)]) * 4
        success_rate = (total_score / max_score * 100) if max_score > 0 else 0
        
        links_provided = len([r for r in results if r.get('has_links', False)])
        web_searches = len([r for r in results if r.get('web_enhanced', False)])
        
        print(f"🎯 Puntuación total: {total_score}/{max_score} ({success_rate:.1f}%)")
        print(f"🔗 Respuestas con enlaces oficiales: {links_provided}/{len(results)}")
        print(f"🌐 Búsquedas web realizadas: {web_searches}/{len(results)}")
        
        # Estadísticas del chatbot
        stats = chatbot.session_stats
        print(f"\n📈 Estadísticas de la sesión:")
        print(f"  Preguntas procesadas: {stats['questions_asked']}")
        print(f"  Respuestas exitosas: {stats['successful_responses']}")
        print(f"  Enlaces sugeridos: {stats['links_suggested']}")
        print(f"  Búsquedas web: {stats['web_searches_used']}")
        
        # Recomendaciones
        print(f"\n💡 Evaluación del sistema:")
        if success_rate >= 80:
            print("🟢 ¡Sistema funcionando excelentemente!")
        elif success_rate >= 60:
            print("🟡 Sistema funcionando bien, con margen de mejora")
        else:
            print("🔴 Sistema necesita optimización")
        
        print(f"\n🔗 Sistema de enlaces: {'Funcionando' if links_provided > 0 else 'Necesita revisión'}")
        print(f"🌐 Sistema web: {'Funcionando' if web_searches > 0 else 'Necesita revisión'}")
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_complete_system()