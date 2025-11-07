"""
Test directo de la vista del chatbot Django
"""

import os
import sys
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cross_project.settings')

# Agregar el directorio del proyecto al path
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.append(project_dir)

django.setup()

from django.test import RequestFactory
from cross_asistent.chatbot import chatbot

def test_django_chatbot_view():
    """Probar la vista del chatbot directamente"""
    print("🧪 PROBANDO VISTA DEL CHATBOT DJANGO")
    print("=" * 45)
    
    # Crear factory de requests
    factory = RequestFactory()
    
    # Preguntas de prueba
    test_questions = [
        "¿Quién es el rector?",
        "¿Qué carreras ofrece la UTC?", 
        "¿Cuándo es la ceremonia de graduación?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. 👤 Pregunta: {question}")
        
        # Crear request POST como lo haría el frontend
        request_data = json.dumps({'question': question})
        request = factory.post(
            '/chatbot/',
            data=request_data,
            content_type='application/json'
        )
        
        try:
            # Llamar a la vista del chatbot
            response = chatbot(request)
            
            if response.status_code == 200:
                response_data = json.loads(response.content.decode('utf-8'))
                
                if response_data.get('success'):
                    answer = response_data.get('answer', {})
                    informacion = answer.get('informacion', 'Sin respuesta')
                    
                    # Mostrar solo primeras 100 caracteres
                    if len(informacion) > 100:
                        informacion = informacion[:100] + "..."
                    
                    print(f"🤖 FALCON: {informacion}")
                    print(f"   ✅ Éxito | Gemini: {answer.get('gemini_powered', 'Unknown')}")
                    
                    # Si hay contexto, mostrarlo
                    if 'context_items' in answer:
                        print(f"   📊 Contexto: {answer['context_items']} items")
                else:
                    print(f"❌ Error: {response_data.get('message', 'Unknown')}")
            else:
                print(f"❌ Error HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Excepción: {e}")
    
    print("\n" + "=" * 45)
    print("🎯 Si ves respuestas correctas aquí, el problema es en el frontend")

if __name__ == "__main__":
    test_django_chatbot_view()