#!/usr/bin/env python3
"""
Script para probar que FALCON responda correctamente a preguntas específicas
"""

import requests
import json
import time

def test_specific_responses():
    """Probar respuestas específicas de FALCON"""
    print("🎯 PROBANDO RESPUESTAS ESPECÍFICAS DE FALCON")
    print("=" * 60)
    
    # URL del chatbot
    url = 'http://127.0.0.1:8000/chatbot/'
    
    # Headers necesarios
    headers = {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    # Casos de prueba específicos
    test_cases = [
        {
            'pregunta': 'que hace la IA',
            'esperado_contenido': ['asistente', 'ayudarte', 'información', 'UTC'],
            'no_deberia_contener': ['carrera de', 'programa académico', 'TSU']
        },
        {
            'pregunta': 'para que sirve FALCON',
            'esperado_contenido': ['guía', 'simplificar', 'acceso', 'información'],
            'no_deberia_contener': ['machine learning', 'deep learning']
        },
        {
            'pregunta': 'que carreras tienen',
            'esperado_contenido': ['carreras', 'programas', 'Inteligencia Artificial'],
            'no_deberia_contener': []
        },
        {
            'pregunta': 'quien es el rector',
            'esperado_contenido': ['Sergio Alberto Guadarrama', 'rector'],
            'no_deberia_contener': ['asistente', 'FALCON']
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. PREGUNTA: '{test['pregunta']}'")
        print("-" * 50)
        
        try:
            # Hacer petición
            response = requests.post(
                url,
                json={'message': test['pregunta']},
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('response', 'Sin respuesta')
                
                print(f"FALCON: {answer[:200]}{'...' if len(answer) > 200 else ''}")
                
                # Verificar contenido esperado
                print("\nANÁLISIS:")
                
                # Contenido que SÍ debería tener
                for expected in test['esperado_contenido']:
                    if expected.lower() in answer.lower():
                        print(f"  ✅ Contiene: '{expected}'")
                    else:
                        print(f"  ❌ Falta: '{expected}'")
                
                # Contenido que NO debería tener
                for unwanted in test['no_deberia_contener']:
                    if unwanted.lower() in answer.lower():
                        print(f"  ❌ Contiene (no debería): '{unwanted}'")
                    else:
                        print(f"  ✅ No contiene: '{unwanted}'")
                
                # Verificar relevancia general
                if len(answer) > 50:
                    print(f"  ✅ Respuesta completa ({len(answer)} caracteres)")
                else:
                    print(f"  ⚠️  Respuesta muy corta ({len(answer)} caracteres)")
                
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # Pausa entre pruebas
        if i < len(test_cases):
            time.sleep(3)
    
    print(f"\n{'='*60}")
    print("🏆 ANÁLISIS COMPLETADO")
    print("Las respuestas ahora deberían ser más precisas y relevantes")

if __name__ == "__main__":
    test_specific_responses()