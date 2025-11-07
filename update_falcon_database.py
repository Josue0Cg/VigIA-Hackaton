#!/usr/bin/env python3
"""
Script para actualizar la base de datos con información nueva de FALCON
"""

import os
import sys
import django
import json
from django.conf import settings

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cross_project.settings')
django.setup()

# Ahora importar después de configurar Django
from cross_asistent.models import Database

def update_falcon_database():
    """Actualizar base de datos con información nueva de FALCON"""
    print("🔄 ACTUALIZANDO BASE DE DATOS DE FALCON")
    print("=" * 50)
    
    # Nuevas entradas para la base de datos
    new_entries = [
        {
            'titulo': 'FALCON - Asistente Virtual Especializado UTC',
            'informacion': 'Soy FALCON, tu asistente virtual especializado de la Universidad Tecnológica de Coahuila. Estoy diseñado con inteligencia artificial avanzada para proporcionarte información precisa y actualizada sobre nuestros programas académicos, incluyendo nuestra nueva carrera de Inteligencia Artificial, trámites administrativos, admisiones, becas y todo lo relacionado con nuestra institución educativa. Mi objetivo es facilitar tu acceso a la información y ayudarte en tu proceso académico.',
            'categoria': 'Asistente'
        },
        {
            'titulo': 'Carrera de Inteligencia Artificial - UTC 2025',
            'informacion': 'La Universidad Tecnológica de Coahuila ahora ofrece la innovadora carrera de Inteligencia Artificial, diseñada para formar profesionales especializados en las tecnologías emergentes del futuro. Este programa académico abarca áreas como machine learning, deep learning, procesamiento de lenguaje natural, visión por computadora y robótica inteligente. Los egresados estarán preparados para desarrollar soluciones innovadoras en sectores como la industria 4.0, salud digital, fintech y automatización. La carrera incluye tanto la modalidad TSU (2 años) como Ingeniería (3 años 8 meses), con laboratorios especializados y convenios con empresas tecnológicas líderes.',
            'categoria': 'Carreras'
        },
        {
            'titulo': 'Programas Académicos Innovadores UTC 2025',
            'informacion': 'Para 2025, la UTC ha expandido su oferta académica con programas innovadores que responden a las demandas del mercado laboral actual. Destacan: Inteligencia Artificial, Ciberseguridad, Desarrollo de Software, Energías Renovables, y Biotecnología Avanzada. Todos estos programas cuentan con instalaciones de última generación, laboratorios especializados y convenios con empresas líderes en cada sector. Nuestro enfoque se centra en la formación práctica y el desarrollo de competencias digitales esenciales para la industria 4.0.',
            'categoria': 'Carreras'
        },
        {
            'titulo': 'Laboratorios de Tecnologías Emergentes UTC',
            'informacion': 'La UTC cuenta con laboratorios de tecnologías emergentes equipados con: estaciones de trabajo para desarrollo de IA, servidores con GPUs para machine learning, equipos de realidad virtual y aumentada, impresoras 3D industriales, y sistemas robóticos avanzados. Estos espacios permiten a los estudiantes experimentar con las últimas innovaciones tecnológicas y desarrollar proyectos aplicados en colaboración con la industria local y nacional.',
            'categoria': 'Instalaciones'
        }
    ]
    
    # Agregar o actualizar entradas
    for entry_data in new_entries:
        # Verificar si ya existe una entrada similar
        existing = Database.objects.filter(titulo__icontains=entry_data['titulo'][:30]).first()
        
        if existing:
            # Actualizar entrada existente
            existing.informacion = entry_data['informacion']
            existing.categoria = entry_data['categoria']
            existing.save()
            print(f"✅ Actualizado: {entry_data['titulo'][:50]}...")
        else:
            # Crear nueva entrada
            new_entry = Database.objects.create(
                titulo=entry_data['titulo'],
                informacion=entry_data['informacion'],
                categoria=entry_data['categoria']
            )
            print(f"➕ Agregado: {entry_data['titulo'][:50]}...")
    
    # Actualizar entradas existentes que mencionen "Hawky"
    print("\n🔄 Actualizando referencias a Hawky...")
    hawky_entries = Database.objects.filter(
        informacion__icontains='hawky'
    ) | Database.objects.filter(
        informacion__icontains='howki'
    )
    
    for entry in hawky_entries:
        # Actualizar contenido
        entry.informacion = entry.informacion.replace('Hawky', 'FALCON')
        entry.informacion = entry.informacion.replace('hawky', 'FALCON')
        entry.informacion = entry.informacion.replace('howki', 'FALCON')
        entry.informacion = entry.informacion.replace('Eres un asistente', 'Soy FALCON, un asistente avanzado')
        entry.save()
        print(f"🔄 Actualizado Hawky->FALCON: {entry.titulo[:40]}...")
    
    # Estadísticas finales
    total_entries = Database.objects.count()
    falcon_entries = Database.objects.filter(informacion__icontains='FALCON').count()
    
    print(f"\n📊 RESUMEN:")
    print(f"   Total de entradas: {total_entries}")
    print(f"   Entradas con FALCON: {falcon_entries}")
    print(f"   Nuevas entradas agregadas: {len(new_entries)}")
    print(f"   Referencias Hawky actualizadas: {hawky_entries.count()}")
    
    print(f"\n🎯 ¡Base de datos actualizada exitosamente!")
    print("=" * 50)

if __name__ == "__main__":
    update_falcon_database()