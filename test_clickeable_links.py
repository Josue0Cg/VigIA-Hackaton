#!/usr/bin/env python3
"""
Test para verificar que los enlaces se devuelven correctamente en las respuestas
"""

import requests
import json

def test_chatbot_links():
    """Probar que el chatbot devuelve enlaces en las respuestas"""
    
    print("🔗 PRUEBA DE ENLACES CLICKEABLES EN CHATBOT")
    print("="*60)
    
    url = "http://127.0.0.1:8000/chatbot/"
    
    # Preguntas que deben devolver enlaces
    test_questions = [
        "¿Tienes algún enlace de la UTC?",
        "¿Cuál es el sitio web oficial de la UTC?",
        "links de la utc",
        "¿Dónde puedo ver las carreras?"
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
                    # En lugar de 'message', usar la clave correcta
                    answer_key = 'message' if 'message' in result else 'answer'
                    if answer_key in result:
                        if isinstance(result[answer_key], dict):
                            answer_text = result[answer_key].get('informacion', str(result[answer_key]))
                        else:
                            answer_text = str(result[answer_key])
                        
                        print(f"🤖 RESPUESTA: {answer_text}")
                        
                        # Verificar si contiene URLs
                        has_url = 'https://' in answer_text or 'http://' in answer_text
                        has_utc_link = 'utc.edu.mx' in answer_text
                        
                        if has_url and has_utc_link:
                            print("✅ ¡Respuesta contiene URLs de UTC!")
                            print("💡 El JavaScript debería convertirlos en enlaces clickeables")
                        elif has_url:
                            print("⚠️ Contiene URLs pero no son de UTC")
                        else:
                            print("❌ No contiene URLs")
                    else:
                        print(f"⚠️ Estructura de respuesta inesperada: {list(result.keys())}")
                        
                else:
                    print(f"❌ Error en respuesta: {result}")
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error en solicitud: {e}")
    
    print(f"\n{'='*60}")
    print("✅ Prueba completada")
    print("💡 Los URLs en las respuestas deberían aparecer como enlaces clickeables en el navegador")

if __name__ == "__main__":
    test_chatbot_links()