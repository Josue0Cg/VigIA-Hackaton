#!/usr/bin/env python3
"""
Sistema para agregar información específica sobre transporte UTC
"""

import json
import os

def add_transport_information():
    """Agrega información específica sobre transporte a la base de datos"""
    
    # Cargar datos existentes
    data_file = 'exported_data/utc_training_data_20251105_192821.json'
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            training_data = json.load(f)
    except FileNotFoundError:
        print("❌ No se encontró el archivo de datos")
        return
    
    # Nueva información sobre transporte
    transport_entries = [
        {
            "pregunta": "¿La UTC tiene transporte para estudiantes?",
            "respuesta": "Actualmente la UTC no cuenta con un servicio de transporte directo para estudiantes. Sin embargo, la universidad está ubicada en una zona accesible por transporte público. Te recomiendo consultar en el departamento de servicios estudiantiles para conocer las opciones de movilidad disponibles y posibles convenios con empresas de transporte.",
            "categoria": "servicios",
            "palabras_clave": ["transporte", "movilidad", "servicios estudiantiles", "transporte público"]
        },
        {
            "pregunta": "¿Cómo llegar a la UTC en transporte público?",
            "respuesta": "La UTC está ubicada en una zona accesible por diferentes rutas de transporte público. Para obtener información detallada sobre las rutas específicas, horarios y paradas más cercanas a la universidad, te sugiero consultar directamente en el departamento de servicios estudiantiles o en la administración, ya que ellos manejan la información más actualizada sobre las opciones de transporte disponibles.",
            "categoria": "ubicacion",
            "palabras_clave": ["transporte público", "rutas", "ubicación", "cómo llegar", "movilidad"]
        },
        {
            "pregunta": "¿Hay convenios de transporte con empresas para estudiantes UTC?",
            "respuesta": "Para información sobre posibles convenios de transporte con empresas o descuentos especiales para estudiantes de UTC, es recomendable consultar directamente en el departamento de servicios estudiantiles. Ellos pueden proporcionarte detalles actualizados sobre acuerdos vigentes y opciones de movilidad que beneficien a la comunidad estudiantil.",
            "categoria": "servicios",
            "palabras_clave": ["convenios", "descuentos", "empresas transporte", "servicios estudiantiles"]
        }
    ]
    
    # Agregar nuevas entradas
    training_data.extend(transport_entries)
    
    # Guardar archivo actualizado
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Se agregaron {len(transport_entries)} nuevas entradas sobre transporte")
    print(f"📊 Total de entradas: {len(training_data)}")
    
    return len(training_data)

if __name__ == "__main__":
    add_transport_information()