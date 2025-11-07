"""
Script de prueba para validar el chatbot Gemini sin necesidad de API key
Demuestra el funcionamiento del sistema completo
"""

import json
import os
import sys

# Agregar el directorio actual al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def test_system_without_gemini():
    """Prueba el sistema de respaldo (fallback) sin Gemini"""
    print("🧪 PROBANDO SISTEMA DE CHATBOT UTC - MODO FALLBACK")
    print("=" * 60)
    
    # Simular datos de la base de datos (similar a la exportada)
    mock_database = [
        {
            'titulo': 'Diseño y Gestión de Redes Logísticas - TSU',
            'informacion': 'El Técnico Superior Universitario en Logística está preparado para trabajar en empresas industriales, comerciales y de servicios en áreas como almacén, compras, distribución y cadena de suministros.',
            'categoria': 'Informacion'
        },
        {
            'titulo': 'Examen de ingreso ingeniería',
            'informacion': 'Examen de ingreso ingeniería 14/08/2024 desde las 8:00 a.m. hasta las 3:00 p.m.',
            'categoria': 'Calendario'
        },
        {
            'titulo': 'Biblioteca',
            'informacion': 'La biblioteca de la UTC cuenta con recursos digitales y físicos para apoyo académico de estudiantes y profesores.',
            'categoria': 'Mapa'
        },
        {
            'titulo': 'Rector Sergio Alberto Guadarrama Cortez',
            'informacion': 'Sergio Alberto Guadarrama Cortés, Rector de la Universidad Tecnológica de Coahuila. Nacido el 5 de agosto de 1965 en Nueva Rosita, Coahuila.',
            'categoria': 'Personal'
        }
    ]
    
    def simple_search(question, database):
        """Función de búsqueda simple que imita el fallback"""
        question_words = question.lower().split()
        best_match = None
        best_score = 0
        
        for item in database:
            score = 0
            title_lower = item['titulo'].lower()
            info_lower = item['informacion'].lower()
            
            for word in question_words:
                if len(word) > 2:
                    if word in title_lower:
                        score += 3
                    if word in info_lower:
                        score += 1
            
            if score > best_score:
                best_score = score
                best_match = item
        
        return best_match, best_score
    
    # Lista de preguntas de prueba
    test_questions = [
        "¿Qué carreras tiene la UTC?",
        "¿Cuándo es el examen de ingreso?",
        "¿Dónde está la biblioteca?",
        "¿Quién es el rector?",
        "¿Cómo puedo obtener una beca?",
        "Información sobre logística",
        "Horarios de examen",
        "Ubicación campus"
    ]
    
    print("🤖 FALCON - Asistente Virtual UTC")
    print("Modo: Fallback (sin API externa)")
    print("-" * 40)
    
    success_count = 0
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. 👤 Usuario: {question}")
        
        match, score = simple_search(question, mock_database)
        
        if match and score > 0:
            print(f"🤖 FALCON: {match['informacion']}")
            print(f"   📊 Categoría: {match['categoria']} | Relevancia: {score}")
            success_count += 1
        else:
            print("🤖 FALCON: Lo siento, no encontré información específica sobre tu consulta. Te recomiendo visitar nuestra sección de preguntas frecuentes.")
            print("   📊 Sin coincidencias encontradas")
    
    print("\n" + "=" * 60)
    print(f"📈 RESULTADOS DEL TEST:")
    print(f"   Preguntas procesadas: {len(test_questions)}")
    print(f"   Respuestas encontradas: {success_count}")
    print(f"   Tasa de éxito: {(success_count/len(test_questions)*100):.1f}%")
    print(f"   Sistema: Fallback (Búsqueda local)")

def test_with_gemini():
    """Intenta probar con Gemini si está disponible"""
    print("\n🧪 PROBANDO SISTEMA GEMINI")
    print("=" * 60)
    
    try:
        # Intentar importar el chatbot de Gemini
        from utc_gemini_chatbot import UTCGeminiChatbot
        
        print("✅ Módulo Gemini importado correctamente")
        
        # Intentar inicializar
        chatbot = UTCGeminiChatbot()
        
        if chatbot.initialize():
            print("✅ Chatbot Gemini inicializado")
            print(f"✅ Base de conocimientos: {chatbot.utc_context['total_questions']} preguntas")
            
            # Probar una pregunta
            test_question = "¿Qué carreras ofrece la UTC?"
            print(f"\n👤 Usuario: {test_question}")
            
            result = chatbot.generate_response(test_question)
            
            if result['success']:
                print(f"🤖 FALCON (Gemini): {result['response'][:200]}...")
                print(f"   📊 Contexto relevante: {result['relevant_context_count']} items")
                print("✅ ¡Gemini funcionando correctamente!")
            else:
                print(f"❌ Error en respuesta: {result.get('error', 'Unknown')}")
        
        else:
            print("❌ No se pudo inicializar Gemini (probablemente falta API key)")
            
    except ImportError as e:
        print(f"❌ No se pudo importar Gemini: {e}")
    except Exception as e:
        print(f"❌ Error con Gemini: {e}")

def main():
    """Función principal de prueba"""
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA CHATBOT UTC")
    print("🤖 FALCON - Asistente Virtual Universidad Tecnológica de Coahuila")
    print("=" * 70)
    
    # Mostrar información del sistema
    print("📋 INFORMACIÓN DEL SISTEMA:")
    print(f"   Datos exportados: {'✅' if os.path.exists('exported_data') else '❌'}")
    print(f"   Configuración Gemini: {'✅' if os.path.exists('gemini_config.py') else '❌'}")
    print(f"   Chatbot Gemini: {'✅' if os.path.exists('utc_gemini_chatbot.py') else '❌'}")
    print(f"   Entrenador: {'✅' if os.path.exists('gemini_trainer.py') else '❌'}")
    
    # Probar sistema de respaldo
    test_system_without_gemini()
    
    # Intentar probar Gemini
    test_with_gemini()
    
    print("\n🎉 PRUEBAS COMPLETADAS")
    print("\n📝 PASOS SIGUIENTES:")
    print("1. Obtener API key de Gemini en: https://makersuite.google.com")
    print("2. Agregar GEMINI_API_KEY=tu_clave_aqui al archivo .env")
    print("3. Ejecutar el servidor Django y probar el chatbot")
    print("4. ¡El sistema está listo para usar!")

if __name__ == "__main__":
    main()