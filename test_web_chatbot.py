#!/usr/bin/env python3
"""
Test web directo para verificar que el chatbot Django está funcionando correctamente
"""

import requests
import json

def test_web_chatbot():
    """Probar el chatbot web directamente"""
    
    print("🌐 PRUEBA DIRECTA DEL CHATBOT WEB")
    print("="*60)
    
    url = "http://127.0.0.1:8000/chatbot/"
    
    # Preguntas específicas sobre transporte
    test_questions = [
        "¿La UTC tiene transporte para estudiantes?",
        "¿Cómo llego a la UTC en transporte público?",
        "¿Hay descuentos de transporte para estudiantes?",
        "¿Dónde está ubicada la UTC exactamente?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*50}")
        print(f"📝 PREGUNTA {i}: {question}")
        print(f"{'='*50}")
        
        try:
            # Enviar solicitud POST
            payload = {"question": question}
            headers = {"Content-Type": "application/json"}
            
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success', False):
                    answer = result.get('message', 'Sin respuesta')
                    print(f"🤖 RESPUESTA: {answer}")
                    
                    # Verificar si usa información específica
                    specific_keywords = [
                        'no cuenta con un servicio',
                        'departamento de servicios estudiantiles',
                        'zona accesible',
                        'consultar directamente',
                        'coahuila'
                    ]
                    
                    if any(keyword in answer.lower() for keyword in specific_keywords):
                        print("✅ ¡Respuesta específica de la base de datos!")
                    else:
                        print("⚠️ Respuesta parece genérica o con enlaces")
                        
                    # Verificar si sugiere enlaces oficiales (no deseado para estas preguntas)
                    if 'tienes algún link' in answer.lower() or 'página oficial' in answer.lower():
                        print("❌ Está sugiriendo enlaces cuando debería usar datos específicos")
                    
                else:
                    print(f"❌ Error en respuesta: {result.get('message', 'Error desconocido')}")
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error en solicitud: {e}")
    
    print(f"\n{'='*60}")
    print("✅ Prueba web completada")

if __name__ == "__main__":
    test_web_chatbot()