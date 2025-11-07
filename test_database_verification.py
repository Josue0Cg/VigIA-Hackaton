#!/usr/bin/env python3
"""
Test directo de la base de datos actualizada
"""

import json
import os

def test_database_content():
    """Verificar que la base de datos tiene las nuevas entradas"""
    
    data_file = 'exported_data/utc_training_data_20251105_192821.json'
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Total de entradas en la base de datos: {len(data)}")
        
        # Buscar entradas sobre transporte
        transport_entries = []
        for entry in data:
            if any(keyword in entry.get('pregunta', '').lower() for keyword in 
                   ['transporte', 'transportes', 'ubicada', 'ubicación']):
                transport_entries.append(entry)
        
        print(f"🚌 Entradas sobre transporte encontradas: {len(transport_entries)}")
        
        for i, entry in enumerate(transport_entries, 1):
            print(f"\n📝 ENTRADA {i}:")
            print(f"Pregunta: {entry['pregunta']}")
            print(f"Respuesta: {entry['respuesta'][:100]}...")
            print(f"Categoría: {entry.get('categoria', 'N/A')}")
            if 'fecha_agregado' in entry:
                print(f"Fecha agregado: {entry['fecha_agregado']}")
        
        return len(data), len(transport_entries)
        
    except FileNotFoundError:
        print("❌ Archivo de datos no encontrado")
        return 0, 0
    except Exception as e:
        print(f"❌ Error leyendo datos: {e}")
        return 0, 0

def test_gemini_config():
    """Probar la configuración de Gemini"""
    try:
        from gemini_config import GeminiConfig
        
        # Cargar contexto
        context = GeminiConfig.load_utc_context()
        print(f"📚 Contexto UTC cargado: {context.get('total_questions', 0)} preguntas")
        
        # Verificar categorías
        categories = context.get('categories', {})
        print(f"📂 Categorías disponibles: {list(categories.keys())}")
        
        # Buscar categorías relacionadas con servicios o ubicación
        relevant_categories = []
        for cat_name, items in categories.items():
            if any(keyword in cat_name.lower() for keyword in ['servicio', 'ubicacion', 'ubicación']):
                relevant_categories.append((cat_name, len(items)))
        
        if relevant_categories:
            print(f"🎯 Categorías relevantes para transporte:")
            for cat_name, count in relevant_categories:
                print(f"  - {cat_name}: {count} entradas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración Gemini: {e}")
        return False

if __name__ == "__main__":
    print("🔍 VERIFICACIÓN DE BASE DE DATOS ACTUALIZADA")
    print("="*60)
    
    # Test 1: Contenido de la base de datos
    total_entries, transport_entries = test_database_content()
    
    print("\n" + "="*60)
    
    # Test 2: Configuración de Gemini
    config_ok = test_gemini_config()
    
    print("\n" + "="*60)
    print("📋 RESUMEN:")
    print(f"Total de entradas: {total_entries}")
    print(f"Entradas sobre transporte: {transport_entries}")
    print(f"Configuración Gemini: {'✅ OK' if config_ok else '❌ Error'}")
    
    if transport_entries > 0:
        print("✅ ¡La base de datos tiene información sobre transporte!")
    else:
        print("⚠️ No se encontraron entradas sobre transporte")