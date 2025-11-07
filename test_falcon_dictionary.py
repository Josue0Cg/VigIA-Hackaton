#!/usr/bin/env python3
"""
Script de prueba para verificar que FALCON funciona con el sistema de diccionario
"""

import os
import sys
import django
from django.conf import settings

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cross_project.settings')
django.setup()

# Ahora importar después de configurar Django
from cross_asistent.chatbot import search_direct_database, fallback_chatbot

def test_falcon_with_dictionary():
    """Probar FALCON con el sistema de diccionario integrado"""
    print("🚀 PROBANDO FALCON CON SISTEMA DE DICCIONARIO")
    print("=" * 60)
    
    # Casos de prueba para verificar el diccionario
    test_cases = [
        "hola",
        "¿qué carreras tienen?",
        "¿cuánto dura la carrera?",
        "¿dónde está ubicada la universidad?",
        "¿cuáles son los costos?",
        "¿quién es el rector?"
    ]
    
    for i, question in enumerate(test_cases, 1):
        print(f"\n{i}. PREGUNTA: {question}")
        print("-" * 40)
        
        try:
            # Primero probar búsqueda directa en BD
            direct_response = search_direct_database(question)
            
            if direct_response and isinstance(direct_response, dict) and direct_response.get('found'):
                response = direct_response.get('response', 'Sin respuesta')
                confidence = direct_response.get('confidence_score', 0)
                print(f"📊 FUENTE: Base de datos directa (confianza: {confidence})")
            else:
                response = fallback_chatbot(question)
                print("🤖 FUENTE: Gemini AI")
            
            print(f"FALCON: {response}")
            
            # Verificar que no hable en tercera persona
            if isinstance(response, str):
                if 'La UTC tiene' in response or 'La universidad ofrece' in response:
                    print("⚠️  ADVERTENCIA: Respuesta en tercera persona detectada")
                
                # Verificar que use identidad FALCON
                if 'Hawky' in response:
                    print("⚠️  ADVERTENCIA: Identidad incorrecta detectada")
                
                # Verificar enriquecimiento de vocabulario
                if any(phrase in response.lower() for phrase in ['sin duda', 'efectivamente', 'por supuesto', 'te puedo decir', 'déjame informarte', 'especialidad', 'aspectos', 'destacables']):
                    print("✅ Vocabulario enriquecido detectado")
            
            # Verificar identidad FALCON
            if isinstance(response, str) and 'FALCON' in response:
                print("✅ Identidad FALCON confirmada")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
    
    print(f"\n{'='*60}")
    print("🎯 PRUEBA COMPLETA - Verificar respuestas arriba")

if __name__ == "__main__":
    test_falcon_with_dictionary()