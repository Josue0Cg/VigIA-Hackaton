#!/usr/bin/env python3
"""
Verificar que la base de datos tiene entradas con múltiples enlaces
"""

import json
import os

def check_multiple_links_entries():
    """Verificar entradas con múltiples enlaces en la base de datos"""
    
    data_file = 'exported_data/utc_training_data_20251105_192821.json'
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            training_data = json.load(f)
    except FileNotFoundError:
        print("❌ No se encontró el archivo de datos")
        return False
    
    print("🔍 BÚSQUEDA DE ENTRADAS CON MÚLTIPLES ENLACES")
    print("="*60)
    
    # Buscar entradas que contengan múltiples enlaces
    multiple_link_entries = []
    
    for entry in training_data:
        respuesta = entry.get('respuesta', '')
        tipo = entry.get('tipo_enlace', '')
        
        # Buscar entradas que podrían tener múltiples enlaces
        if (('listado' in tipo) or 
            ('🌐' in respuesta) or 
            ('🏠' in respuesta) or 
            (respuesta.count('https://') > 1) or
            ('enlaces oficiales' in entry.get('pregunta', '').lower())):
            
            multiple_link_entries.append({
                'pregunta': entry.get('pregunta'),
                'respuesta': respuesta,
                'tipo': tipo,
                'enlace_count': respuesta.count('https://')
            })
    
    print(f"📊 Total de entradas: {len(training_data)}")
    print(f"🔗 Entradas con múltiples enlaces: {len(multiple_link_entries)}")
    
    if multiple_link_entries:
        print(f"\n📝 ENTRADAS ENCONTRADAS:")
        for i, entry in enumerate(multiple_link_entries, 1):
            print(f"\n{i}. {entry['pregunta']}")
            print(f"   Enlaces encontrados: {entry['enlace_count']}")
            print(f"   Tipo: {entry['tipo']}")
            print(f"   Respuesta (primeros 150 chars): {entry['respuesta'][:150]}...")
    
    return len(multiple_link_entries) > 0

def add_comprehensive_links_entry():
    """Agregar entrada específica con TODOS los enlaces"""
    
    data_file = 'exported_data/utc_training_data_20251105_192821.json'
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            training_data = json.load(f)
    except FileNotFoundError:
        print("❌ No se encontró el archivo de datos")
        return False
    
    # Entrada comprehensiva con TODOS los enlaces
    comprehensive_entry = {
        "pregunta": "enlaces utc",
        "respuesta": "Aquí tienes todos los enlaces oficiales de la Universidad Tecnológica de Coahuila:\n\n🏠 Sitio principal: https://www.utc.edu.mx/\n📚 Carreras y programas: https://www.utc.edu.mx/carreras/\n📝 Admisiones e inscripciones: https://www.utc.edu.mx/admisiones/\n📞 Contacto y ubicación: https://www.utc.edu.mx/contacto/\n🎓 Servicios estudiantiles: https://www.utc.edu.mx/servicios-estudiantiles/\n💰 Costos y colegiaturas: https://www.utc.edu.mx/costos/\n\nTodos estos son enlaces oficiales y actualizados de la universidad.",
        "categoria": "enlaces",
        "palabras_clave": ["enlaces", "links", "utc", "todos", "oficiales", "sitios"],
        "enlace_oficial": "https://www.utc.edu.mx/",
        "tipo_enlace": "listado_completo",
        "fecha_agregado": "2025-11-06T00:00:00",
        "version": "enlaces_completos_v1.0",
        "tiene_enlace_directo": True,
        "multiple_links": True
    }
    
    # Buscar si ya existe una entrada similar
    exists = False
    for entry in training_data:
        if ('enlaces utc' in entry.get('pregunta', '').lower() and 
            entry.get('respuesta', '').count('https://') >= 6):
            exists = True
            print("✅ Ya existe una entrada con múltiples enlaces")
            break
    
    if not exists:
        # Agregar la nueva entrada
        training_data.append(comprehensive_entry)
        
        # Crear backup
        from datetime import datetime
        backup_file = f'exported_data/backup_before_comprehensive_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(training_data[:-1], f, ensure_ascii=False, indent=2)
        
        # Guardar archivo actualizado
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, ensure_ascii=False, indent=2)
        
        print("✅ Agregada entrada comprehensiva con todos los enlaces")
        print(f"📊 Total de entradas: {len(training_data)}")
        print(f"💾 Backup creado: {backup_file}")
        
        return True
    
    return False

if __name__ == "__main__":
    # Verificar entradas existentes
    has_multiple = check_multiple_links_entries()
    
    # Agregar entrada comprehensiva si no existe
    added = add_comprehensive_links_entry()
    
    print(f"\n{'='*60}")
    print("📋 RESUMEN:")
    print(f"Tiene entradas con múltiples enlaces: {'✅ SÍ' if has_multiple else '❌ NO'}")
    print(f"Agregada entrada comprehensiva: {'✅ SÍ' if added else '➖ Ya existía'}")
    
    if has_multiple or added:
        print("🎉 El chatbot debería proporcionar múltiples enlaces cuando se soliciten")