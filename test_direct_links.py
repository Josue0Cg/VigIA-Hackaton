#!/usr/bin/env python3
"""
Test específico para verificar que el chatbot proporciona enlaces directos
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from utc_gemini_chatbot import UTCGeminiChatbot

def test_direct_links():
    """Probar que el chatbot proporciona enlaces directos"""
    
    print("🔗 PRUEBA DE ENLACES DIRECTOS")
    print("="*60)
    
    # Inicializar chatbot
    try:
        chatbot = UTCGeminiChatbot()
        print("✅ Chatbot inicializado correctamente")
    except Exception as e:
        print(f"❌ Error inicializando chatbot: {e}")
        return
    
    # Preguntas específicas que deben devolver enlaces
    link_questions = [
        "¿Tienes algún enlace de la UTC?",
        "¿Tienes el link de alguna página de la UTC?",
        "¿Cuál es el sitio web oficial de la UTC?",
        "¿Dónde puedo ver las carreras de la UTC?",
        "¿Cómo puedo contactar a la UTC?",
        "enlaces de la utc"
    ]
    
    successful_links = 0
    
    for i, question in enumerate(link_questions, 1):
        print(f"\n{'='*50}")
        print(f"📝 PREGUNTA {i}: {question}")
        print(f"{'='*50}")
        
        try:
            result = chatbot.generate_response(question)
            
            if result.get('success', False):
                response = result.get('response', 'Sin respuesta')
                print(f"🤖 RESPUESTA: {response}")
                
                # Verificar si contiene enlaces
                has_url = 'https://' in response or 'http://' in response
                has_utc_link = 'utc.edu.mx' in response
                is_direct_link = result.get('source') == 'database_with_direct_links'
                
                if has_url and has_utc_link:
                    print("✅ ¡Respuesta contiene enlaces oficiales de UTC!")
                    successful_links += 1
                    
                    if is_direct_link:
                        print("🎯 ¡Enlace obtenido directamente de la base de datos!")
                        
                elif has_url:
                    print("⚠️ Contiene enlaces pero no son de UTC")
                else:
                    print("❌ No contiene enlaces")
                
            else:
                print(f"❌ Error en respuesta: {result.get('response', 'Error desconocido')}")
                
        except Exception as e:
            print(f"❌ Error obteniendo respuesta: {e}")
    
    print(f"\n{'='*60}")
    print(f"📊 RESULTADOS:")
    print(f"Preguntas realizadas: {len(link_questions)}")
    print(f"Respuestas con enlaces: {successful_links}")
    print(f"Tasa de éxito: {(successful_links/len(link_questions)*100):.1f}%")
    
    if successful_links >= len(link_questions) * 0.8:  # 80% o más
        print("🎉 ¡Sistema de enlaces funcionando correctamente!")
    else:
        print("⚠️ El sistema necesita ajustes")

def test_database_links():
    """Verificar que la base de datos contiene los enlaces"""
    
    print(f"\n{'='*60}")
    print("🔍 VERIFICACIÓN DE ENLACES EN BASE DE DATOS")
    print("="*60)
    
    try:
        chatbot = UTCGeminiChatbot()
        
        # Buscar entradas con enlaces
        entries_with_links = 0
        total_entries = len(chatbot.utc_context['knowledge_base'])
        
        sample_links = []
        
        for item in chatbot.utc_context['knowledge_base']:
            if item.get('enlace_oficial'):
                entries_with_links += 1
                if len(sample_links) < 3:
                    sample_links.append({
                        'pregunta': item.get('pregunta'),
                        'enlace': item.get('enlace_oficial'),
                        'tipo': item.get('tipo_enlace')
                    })
        
        print(f"📊 Total de entradas: {total_entries}")
        print(f"🔗 Entradas con enlaces: {entries_with_links}")
        print(f"📈 Porcentaje con enlaces: {(entries_with_links/total_entries*100):.1f}%")
        
        if sample_links:
            print(f"\n🔗 EJEMPLOS DE ENLACES EN LA BASE:")
            for i, link in enumerate(sample_links, 1):
                print(f"{i}. {link['pregunta']}")
                print(f"   Enlace: {link['enlace']}")
                print(f"   Tipo: {link['tipo']}")
        
        return entries_with_links > 0
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

if __name__ == "__main__":
    # Test 1: Verificar base de datos
    db_ok = test_database_links()
    
    # Test 2: Probar enlaces directos
    if db_ok:
        test_direct_links()
    else:
        print("❌ No se pueden probar enlaces porque no hay enlaces en la base de datos")