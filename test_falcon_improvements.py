#!/usr/bin/env python3
"""
Script para probar las mejoras de FALCON con respuestas personalizadas
"""

import requests
import json
import time

def test_falcon_improvements():
    """Probar las mejoras de FALCON"""
    print("🚀 PROBANDO MEJORAS DE FALCON")
    print("=" * 60)
    
    # URL del chatbot
    url = 'http://127.0.0.1:8000/chatbot/'
    
    # Headers necesarios
    headers = {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    # Casos de prueba para verificar las mejoras
    test_cases = [
        {
            'pregunta': 'hola',
            'esperado': ['FALCON', 'especializado', 'Inteligencia Artificial']
        },
        {
            'pregunta': 'que eres',
            'esperado': ['FALCON', 'asistente', 'avanzado']
        },
        {
            'pregunta': 'que carreras de IA tienen',
            'esperado': ['Inteligencia Artificial', 'machine learning', 'innovadora']
        },
        {
            'pregunta': 'cuales son las nuevas carreras',
            'esperado': ['programas', 'innovadores', '2025']
        },
        {
            'pregunta': 'quien es el rector',
            'esperado': ['Sergio Alberto Guadarrama', 'rector', 'fundamentals']
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. PREGUNTA: {test['pregunta']}")
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
                
                print(f"FALCON: {answer}")
                
                # Verificar mejoras
                improvements_found = []
                
                # Verificar palabras clave esperadas
                for keyword in test['esperado']:
                    if keyword in answer:
                        improvements_found.append(f"✅ Contiene: '{keyword}'")
                    else:
                        improvements_found.append(f"❌ Falta: '{keyword}'")
                
                # Verificar que no sea "Hawky"
                if 'Hawky' not in answer and 'hawky' not in answer:
                    improvements_found.append("✅ Sin referencias a Hawky")
                else:
                    improvements_found.append("❌ Todavía menciona Hawky")
                
                # Verificar que no hable en tercera persona
                third_person_indicators = ['La UTC tiene', 'La universidad ofrece']
                if not any(indicator in answer for indicator in third_person_indicators):
                    improvements_found.append("✅ No habla en tercera persona")
                else:
                    improvements_found.append("❌ Habla en tercera persona")
                
                # Verificar personalización
                personal_indicators = ['Te puedo decir', 'Nuestra institución', 'Con gusto', 'Te comento']
                if any(indicator in answer for indicator in personal_indicators):
                    improvements_found.append("✅ Respuesta personalizada")
                else:
                    improvements_found.append("⚠️  Puede ser más personalizada")
                
                # Mostrar resultados
                print("ANÁLISIS:")
                for improvement in improvements_found:
                    print(f"  {improvement}")
                
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # Pausa entre pruebas
        if i < len(test_cases):
            time.sleep(2)
    
    print(f"\n{'='*60}")
    print("🎯 PRUEBA COMPLETA DE MEJORAS FALCON")
    print("Revisa los resultados arriba para verificar las mejoras")

if __name__ == "__main__":
    test_falcon_improvements()