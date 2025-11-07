#!/usr/bin/env python3
"""
Test rápido para verificar que el chatbot reconoce las nuevas entradas sobre transporte
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from utc_gemini_chatbot import UTCGeminiChatbot

def test_transport_questions():
    """Probar preguntas específicas sobre transporte"""
    
    print("🧪 PRUEBA DE NUEVAS ENTRADAS SOBRE TRANSPORTE")
    print("="*60)
    
    # Inicializar chatbot
    try:
        chatbot = UTCGeminiChatbot()
        print("✅ Chatbot inicializado correctamente")
    except Exception as e:
        print(f"❌ Error inicializando chatbot: {e}")
        return
    
    # Preguntas sobre transporte
    transport_questions = [
        "¿La UTC tiene transporte para estudiantes?",
        "¿Cómo llego a la UTC en transporte público?",
        "¿Hay descuentos de transporte para estudiantes?",
        "¿Dónde está ubicada la UTC exactamente?",
        "¿La universidad ofrece servicio de transporte?"
    ]
    
    print(f"\n🎯 Probando {len(transport_questions)} preguntas...")
    
    for i, question in enumerate(transport_questions, 1):
        print(f"\n{'='*50}")
        print(f"📝 PREGUNTA {i}: {question}")
        print(f"{'='*50}")
        
        try:
            result = chatbot.generate_response(question)
            response = result.get('response', 'Sin respuesta')
            print(f"🤖 RESPUESTA: {response}")
            
            # Verificar si la respuesta contiene información específica
            if any(keyword in response.lower() for keyword in 
                   ['departamento de servicios estudiantiles', 'consultar', 'no cuenta con', 'coahuila']):
                print("✅ Respuesta contiene información específica UTC")
            else:
                print("⚠️ Respuesta parece genérica")
                
        except Exception as e:
            print(f"❌ Error obteniendo respuesta: {e}")
    
    print(f"\n{'='*60}")
    print("✅ Prueba completada")

if __name__ == "__main__":
    test_transport_questions()