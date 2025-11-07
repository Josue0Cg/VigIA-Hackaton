#!/usr/bin/env python3
"""
Test directo para verificar que el sistema está cargando los datos correctos
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from gemini_config import GeminiConfig

def test_data_loading():
    """Verificar qué datos está cargando realmente el sistema"""
    
    print("🔍 VERIFICANDO CARGA DE DATOS DEL SISTEMA")
    print("="*60)
    
    # Cargar contexto UTC
    context = GeminiConfig.load_utc_context()
    
    print(f"📊 Total de preguntas cargadas: {context.get('total_questions', 0)}")
    
    # Buscar preguntas sobre transporte
    knowledge_base = context.get('knowledge_base', [])
    transport_questions = []
    
    for item in knowledge_base:
        pregunta = item.get('pregunta', '').lower()
        if any(keyword in pregunta for keyword in ['transporte', 'transportes', 'ubicada', 'ubicación']):
            transport_questions.append(item)
    
    print(f"🚌 Preguntas sobre transporte encontradas: {len(transport_questions)}")
    
    if transport_questions:
        print("\n📝 PREGUNTAS SOBRE TRANSPORTE EN EL SISTEMA:")
        for i, item in enumerate(transport_questions[:5], 1):
            print(f"\n{i}. {item.get('pregunta', 'Sin pregunta')}")
            respuesta = item.get('respuesta', 'Sin respuesta')
            print(f"   Respuesta: {respuesta[:100]}...")
            if 'fecha_agregado' in item:
                print(f"   Fecha: {item['fecha_agregado']}")
    else:
        print("❌ NO SE ENCONTRARON preguntas sobre transporte en el sistema!")
        print("🔍 Primeras 5 preguntas en el sistema:")
        for i, item in enumerate(knowledge_base[:5], 1):
            print(f"{i}. {item.get('pregunta', 'Sin pregunta')}")
    
    return len(transport_questions)

def test_gemini_direct():
    """Test directo con Gemini usando los datos cargados"""
    
    print("\n" + "="*60)
    print("🧪 TEST DIRECTO CON GEMINI")
    print("="*60)
    
    try:
        # Inicializar Gemini
        model = GeminiConfig.initialize_gemini()
        context = GeminiConfig.load_utc_context()
        system_prompt = GeminiConfig.get_system_prompt(context)
        
        print("✅ Gemini inicializado correctamente")
        
        # Test con pregunta sobre transporte
        question = "¿La UTC tiene transporte para estudiantes?"
        
        # Buscar en la base de conocimientos
        knowledge_base = context.get('knowledge_base', [])
        relevant_info = []
        
        for item in knowledge_base:
            if 'transporte' in item.get('pregunta', '').lower():
                relevant_info.append(f"P: {item['pregunta']}\nR: {item['respuesta']}")
        
        if relevant_info:
            context_info = "\n\n".join(relevant_info[:3])
            full_prompt = f"{system_prompt}\n\nINFORMACIÓN ESPECÍFICA DISPONIBLE:\n{context_info}\n\nPregunta del usuario: {question}"
        else:
            full_prompt = f"{system_prompt}\n\nPregunta del usuario: {question}"
        
        print(f"\n📝 Pregunta: {question}")
        print(f"📚 Información relevante encontrada: {len(relevant_info)} entradas")
        
        # Generar respuesta
        response = model.generate_content(full_prompt)
        print(f"\n🤖 Respuesta: {response.text}")
        
        # Verificar si usa información específica
        if any(keyword in response.text.lower() for keyword in 
               ['no cuenta con un servicio', 'departamento de servicios', 'zona accesible']):
            print("✅ ¡La respuesta usa información específica de la base de datos!")
            return True
        else:
            print("❌ La respuesta parece genérica")
            return False
            
    except Exception as e:
        print(f"❌ Error en test directo: {e}")
        return False

if __name__ == "__main__":
    # Test 1: Verificar carga de datos
    transport_count = test_data_loading()
    
    # Test 2: Test directo con Gemini
    uses_specific_data = test_gemini_direct()
    
    print("\n" + "="*60)
    print("📋 RESUMEN FINAL:")
    print(f"Preguntas sobre transporte: {transport_count}")
    print(f"Usa datos específicos: {'✅ SÍ' if uses_specific_data else '❌ NO'}")
    
    if transport_count > 0 and uses_specific_data:
        print("🎉 ¡Sistema funcionando correctamente!")
    else:
        print("⚠️ Hay problemas que necesitan resolverse")