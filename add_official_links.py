#!/usr/bin/env python3
"""
Agregar enlaces oficiales específicos directamente a la base de datos
"""

import json
import os
from datetime import datetime

def add_utc_official_links():
    """Agregar enlaces oficiales de la UTC directamente a la base de datos"""
    
    data_file = 'exported_data/utc_training_data_20251105_192821.json'
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            training_data = json.load(f)
    except FileNotFoundError:
        print("❌ No se encontró el archivo de datos")
        return False
    
    # Enlaces oficiales específicos de la UTC
    official_links_entries = [
        {
            "pregunta": "¿Cuál es el sitio web oficial de la UTC?",
            "respuesta": "El sitio web oficial de la Universidad Tecnológica de Coahuila es: https://www.utc.edu.mx/ - Aquí encontrarás información completa sobre carreras, admisiones, trámites y servicios universitarios.",
            "categoria": "enlaces",
            "palabras_clave": ["sitio web", "página oficial", "utc.edu.mx", "enlaces", "sitio"],
            "enlace_oficial": "https://www.utc.edu.mx/",
            "tipo_enlace": "sitio_principal"
        },
        {
            "pregunta": "¿Dónde puedo encontrar información sobre admisiones en la UTC?",
            "respuesta": "Para información sobre admisiones y proceso de ingreso a la UTC, visita: https://www.utc.edu.mx/admisiones/ - Aquí encontrarás requisitos, fechas importantes y el proceso completo de inscripción.",
            "categoria": "enlaces",
            "palabras_clave": ["admisiones", "inscripciones", "ingreso", "requisitos", "proceso"],
            "enlace_oficial": "https://www.utc.edu.mx/admisiones/",
            "tipo_enlace": "admisiones"
        },
        {
            "pregunta": "¿Dónde consulto información sobre las carreras de la UTC?",
            "respuesta": "Para conocer todas las carreras y programas académicos que ofrece la UTC, visita: https://www.utc.edu.mx/carreras/ - Aquí encontrarás detalles de cada carrera, plan de estudios y perfil profesional.",
            "categoria": "enlaces", 
            "palabras_clave": ["carreras", "programas académicos", "plan de estudios", "oferta educativa"],
            "enlace_oficial": "https://www.utc.edu.mx/carreras/",
            "tipo_enlace": "carreras"
        },
        {
            "pregunta": "¿Cómo puedo contactar a la UTC?",
            "respuesta": "Para contactar a la Universidad Tecnológica de Coahuila, visita: https://www.utc.edu.mx/contacto/ - Aquí encontrarás teléfonos, direcciones, correos electrónicos y ubicación del campus.",
            "categoria": "enlaces",
            "palabras_clave": ["contacto", "teléfono", "dirección", "ubicación", "correo"],
            "enlace_oficial": "https://www.utc.edu.mx/contacto/",
            "tipo_enlace": "contacto"
        },
        {
            "pregunta": "¿Dónde encuentro información sobre servicios estudiantiles de la UTC?",
            "respuesta": "Para información sobre servicios estudiantiles (becas, biblioteca, deportes, etc.), visita: https://www.utc.edu.mx/servicios-estudiantiles/ - Aquí encontrarás todos los servicios disponibles para estudiantes.",
            "categoria": "enlaces",
            "palabras_clave": ["servicios estudiantiles", "becas", "biblioteca", "deportes", "servicios"],
            "enlace_oficial": "https://www.utc.edu.mx/servicios-estudiantiles/",
            "tipo_enlace": "servicios"
        },
        {
            "pregunta": "¿Tienes algún enlace o link de la UTC?",
            "respuesta": "¡Por supuesto! Aquí tienes los enlaces oficiales principales de la UTC:\n\n🌐 Sitio principal: https://www.utc.edu.mx/\n📚 Carreras: https://www.utc.edu.mx/carreras/\n📝 Admisiones: https://www.utc.edu.mx/admisiones/\n📞 Contacto: https://www.utc.edu.mx/contacto/\n🎓 Servicios estudiantiles: https://www.utc.edu.mx/servicios-estudiantiles/",
            "categoria": "enlaces",
            "palabras_clave": ["enlace", "link", "página", "sitio", "web", "url"],
            "enlace_oficial": "https://www.utc.edu.mx/",
            "tipo_enlace": "listado_completo"
        },
        {
            "pregunta": "¿Tienes el link de alguna página de la UTC?",
            "respuesta": "Sí, aquí están los enlaces oficiales de la UTC:\n\n🏠 Página principal: https://www.utc.edu.mx/\n📖 Información de carreras: https://www.utc.edu.mx/carreras/\n📋 Proceso de admisión: https://www.utc.edu.mx/admisiones/\n📱 Datos de contacto: https://www.utc.edu.mx/contacto/\n\nTodos estos son enlaces oficiales y actualizados de la universidad.",
            "categoria": "enlaces",
            "palabras_clave": ["link", "página", "enlace", "sitio web", "url", "página de la utc"],
            "enlace_oficial": "https://www.utc.edu.mx/",
            "tipo_enlace": "listado_principal"
        },
        {
            "pregunta": "¿Dónde puedo ver información sobre costos y colegiaturas de la UTC?",
            "respuesta": "Para información sobre costos, colegiaturas y pagos en la UTC, visita: https://www.utc.edu.mx/costos/ - Aquí encontrarás detalles sobre cuotas, formas de pago y opciones de financiamiento.",
            "categoria": "enlaces",
            "palabras_clave": ["costos", "colegiaturas", "pagos", "cuotas", "precios"],
            "enlace_oficial": "https://www.utc.edu.mx/costos/",
            "tipo_enlace": "costos"
        }
    ]
    
    # Agregar timestamp y versión a cada entrada
    for entry in official_links_entries:
        entry["fecha_agregado"] = datetime.now().isoformat()
        entry["version"] = "enlaces_oficiales_v1.0"
        entry["tiene_enlace_directo"] = True
    
    # Agregar las nuevas entradas
    training_data.extend(official_links_entries)
    
    # Crear backup
    backup_file = f'exported_data/backup_antes_enlaces_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(training_data[:-len(official_links_entries)], f, ensure_ascii=False, indent=2)
    
    # Guardar archivo actualizado
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Se agregaron {len(official_links_entries)} entradas con enlaces oficiales")
    print(f"📊 Total de entradas: {len(training_data)}")
    print(f"💾 Backup creado: {backup_file}")
    
    return True

def update_existing_entries_with_links():
    """Actualizar entradas existentes para incluir enlaces cuando sea apropiado"""
    
    data_file = 'exported_data/utc_training_data_20251105_192821.json'
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            training_data = json.load(f)
    except FileNotFoundError:
        print("❌ No se encontró el archivo de datos")
        return False
    
    updates_count = 0
    
    # Actualizar entradas existentes que deberían incluir enlaces
    for entry in training_data:
        pregunta = entry.get('pregunta', '').lower()
        respuesta = entry.get('respuesta', '')
        
        # Si la pregunta es sobre información general y no tiene enlace
        if not entry.get('enlace_oficial'):
            if any(keyword in pregunta for keyword in ['información', 'más detalles', 'conocer más', 'sitio', 'página']):
                if 'carreras' in pregunta:
                    entry['enlace_oficial'] = 'https://www.utc.edu.mx/carreras/'
                    entry['tipo_enlace'] = 'carreras'
                    updates_count += 1
                elif 'admision' in pregunta or 'inscripc' in pregunta:
                    entry['enlace_oficial'] = 'https://www.utc.edu.mx/admisiones/'
                    entry['tipo_enlace'] = 'admisiones'
                    updates_count += 1
                elif 'contacto' in pregunta or 'ubicac' in pregunta:
                    entry['enlace_oficial'] = 'https://www.utc.edu.mx/contacto/'
                    entry['tipo_enlace'] = 'contacto'
                    updates_count += 1
                elif 'costo' in pregunta or 'precio' in pregunta:
                    entry['enlace_oficial'] = 'https://www.utc.edu.mx/costos/'
                    entry['tipo_enlace'] = 'costos'
                    updates_count += 1
    
    # Guardar si hubo actualizaciones
    if updates_count > 0:
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, ensure_ascii=False, indent=2)
        
        print(f"🔄 Se actualizaron {updates_count} entradas existentes con enlaces")
    
    return updates_count > 0

def test_links_in_database():
    """Verificar que los enlaces se agregaron correctamente"""
    
    data_file = 'exported_data/utc_training_data_20251105_192821.json'
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            training_data = json.load(f)
    except FileNotFoundError:
        print("❌ No se encontró el archivo de datos")
        return
    
    # Buscar entradas con enlaces
    entries_with_links = []
    for entry in training_data:
        if entry.get('enlace_oficial') or entry.get('tiene_enlace_directo'):
            entries_with_links.append(entry)
    
    print(f"\n📋 VERIFICACIÓN DE ENLACES EN LA BASE DE DATOS")
    print(f"Total de entradas: {len(training_data)}")
    print(f"Entradas con enlaces: {len(entries_with_links)}")
    
    if entries_with_links:
        print(f"\n🔗 ENLACES ENCONTRADOS:")
        for i, entry in enumerate(entries_with_links[:5], 1):
            print(f"\n{i}. {entry.get('pregunta', 'Sin pregunta')}")
            print(f"   Enlace: {entry.get('enlace_oficial', 'Sin enlace')}")
            print(f"   Tipo: {entry.get('tipo_enlace', 'Sin tipo')}")
    
    return len(entries_with_links)

if __name__ == "__main__":
    print("🔗 AGREGANDO ENLACES OFICIALES A LA BASE DE DATOS")
    print("="*60)
    
    # Paso 1: Agregar entradas nuevas con enlaces
    if add_utc_official_links():
        print("✅ Entradas con enlaces agregadas exitosamente")
    
    # Paso 2: Actualizar entradas existentes
    if update_existing_entries_with_links():
        print("✅ Entradas existentes actualizadas con enlaces")
    
    # Paso 3: Verificar resultados
    links_count = test_links_in_database()
    
    print(f"\n{'='*60}")
    print(f"🎉 PROCESO COMPLETADO")
    print(f"Enlaces oficiales agregados a la base de datos: {links_count}")
    print(f"¡El chatbot ahora puede proporcionar enlaces directos!")