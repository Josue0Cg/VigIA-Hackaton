"""
Test para simular exactamente lo que hace el frontend
"""
import requests
import json
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cross_project.settings')
django.setup()

def test_frontend_simulation():
    """Simular la petición exacta que hace el frontend"""
    
    # URL del chatbot (ajustar el puerto si es necesario)
    url = "http://127.0.0.1:8000/chatbot/"
    
    # Datos que envía el frontend
    test_questions = [
        "¿Quién es el rector?",
        "¿Qué carreras ofrece la UTC?",
        "¿Cuándo es la ceremonia de graduación?"
    ]
    
    print("🌐 SIMULANDO PETICIÓN DEL FRONTEND")
    print("=" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. 👤 Pregunta: {question}")
        
        try:
            # Datos en el formato exacto del frontend
            data = {"question": question}
            
            # Headers que envía el frontend
            headers = {
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                # Nota: En una prueba real necesitaríamos el CSRF token
            }
            
            # Hacer la petición POST
            response = requests.post(url, json=data, headers=headers)
            
            print(f"   📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"   ✅ JSON válido recibido")
                    print(f"   🔍 Success: {result.get('success', 'No definido')}")
                    
                    if result.get('success'):
                        answer = result.get('answer', {})
                        informacion = answer.get('informacion', 'No hay información')
                        gemini_powered = answer.get('gemini_powered', False)
                        context_items = answer.get('context_items', 0)
                        
                        print(f"   🤖 Gemini: {gemini_powered}")
                        print(f"   📚 Contexto: {context_items} items")
                        print(f"   💬 Respuesta: {informacion[:100]}...")
                        
                        # Verificar estructura esperada por el frontend
                        required_fields = ['informacion', 'redirigir', 'blank']
                        missing_fields = [field for field in required_fields if field not in answer]
                        
                        if missing_fields:
                            print(f"   ⚠️ Campos faltantes: {missing_fields}")
                        else:
                            print(f"   ✅ Estructura correcta para frontend")
                            
                    else:
                        print(f"   ❌ Error en respuesta: {result.get('message', 'Error desconocido')}")
                        
                except json.JSONDecodeError:
                    print(f"   ❌ Respuesta no es JSON válido")
                    print(f"   📄 Contenido: {response.text[:200]}...")
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                print(f"   📄 Contenido: {response.text[:200]}...")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ No se pudo conectar al servidor")
            print(f"   💡 Asegúrate de que Django esté corriendo en http://127.0.0.1:8000/")
            break
        except Exception as e:
            print(f"   ❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_frontend_simulation()