"""
Test del sistema de respaldo (fallback) cuando Gemini no está disponible
"""

import json

def test_fallback_system():
    """Simular el sistema de respaldo sin Gemini"""
    
    print("🔄 PROBANDO SISTEMA DE RESPALDO (SIN GEMINI)")
    print("=" * 50)
    
    # Simular datos de la base de datos (como en el fallback real)
    mock_database = [
        {
            'titulo': 'Diseño y Gestión de Redes Logísticas - TSU',
            'informacion': 'El Técnico Superior Universitario en Logística está preparado para trabajar en empresas industriales, comerciales y de servicios.',
            'categoria': 'Informacion'
        },
        {
            'titulo': 'Rector Sergio Alberto Guadarrama Cortez',
            'informacion': 'Sergio Alberto Guadarrama Cortés, Rector de la Universidad Tecnológica de Coahuila.',
            'categoria': 'Personal'
        }
    ]
    
    def fallback_search(question, database):
        """Sistema de búsqueda simple (fallback)"""
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
    
    # Preguntas de prueba
    test_questions = [
        "¿Qué carreras de logística hay?",  # Debería encontrar info
        "¿Quién es el rector?",            # Debería encontrar info
        "¿Cuál es la capital de Francia?", # NO debería encontrar nada
        "¿Cómo cocinar pasta?"             # NO debería encontrar nada
    ]
    
    print("🔄 Simulando el sistema cuando Gemini NO está disponible:")
    print("-" * 40)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. 👤 Usuario: {question}")
        
        match, score = fallback_search(question, mock_database)
        
        if match and score > 0:
            print(f"🤖 FALCON (Respaldo): {match['informacion']}")
            print(f"   📊 Relevancia: {score} | Categoría: {match['categoria']}")
        else:
            print("🤖 FALCON (Respaldo): Lo siento, no encontré información específica sobre tu consulta. Te recomiendo visitar nuestra sección de preguntas frecuentes.")
            print("   📊 Sin coincidencias encontradas")
    
    print("\n" + "=" * 50)
    print("🔄 SISTEMA DE 3 NIVELES EXPLICADO:")
    print("\n1️⃣ NIVEL 1 - Búsqueda en Base de Conocimientos:")
    print("   - Busca en 114 preguntas específicas de la UTC")
    print("   - Si encuentra algo relevante → Continúa al Nivel 2")
    print("   - Si no encuentra nada → Va directo al Nivel 3")
    
    print("\n2️⃣ NIVEL 2 - Gemini AI (cuando está disponible):")
    print("   - Usa IA avanzada para responder con contexto")
    print("   - Siempre mantiene identidad como asistente UTC")
    print("   - Para temas fuera de alcance: redirige cortésmente")
    
    print("\n3️⃣ NIVEL 3 - Sistema de Respaldo:")
    print("   - Si Gemini falla o no está disponible")
    print("   - Búsqueda simple en base de datos local")
    print("   - Respuesta estándar si no encuentra nada")
    
    print("\n✅ BENEFICIOS:")
    print("   - El chatbot SIEMPRE funciona (disponibilidad 100%)")
    print("   - Respuestas coherentes incluso sin internet")
    print("   - No inventa información que no tiene")
    print("   - Mantiene profesionalismo en todo momento")

if __name__ == "__main__":
    test_fallback_system()