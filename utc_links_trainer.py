
"""
Sistema de Enlaces Oficiales y Entrenamiento Avanzado para UTC
Proporciona links específicos según el tipo de consulta
"""

import json
import os
from datetime import datetime
from typing import Dict, List

class UTCOfficialLinksTrainer:
    """Sistema para entrenar el chatbot con enlaces oficiales específicos"""
    
    def __init__(self):
        self.official_links = {
            "sitio_principal": "https://utc.edu.mx/",
            "admisiones": "https://utc.edu.mx/admisiones/",
            "servicios_escolares": "https://utc.edu.mx/servicios-escolares/",
            "carreras": "https://utc.edu.mx/carreras/",
            "calendario": "https://utc.edu.mx/calendario/",
            "costos": "https://utc.edu.mx/costos/",
            "contacto": "https://utc.edu.mx/contacto/",
            "noticias": "https://utc.edu.mx/noticias/",
            "vinculacion": "https://utc.edu.mx/vinculacion/",
            "biblioteca": "https://utc.edu.mx/biblioteca/",
            "mi_portal": "https://mi.utc.edu.mx/",
            "plataforma_educativa": "https://plataforma.utc.edu.mx/"
        }
        
        self.link_training_data = [
            {
                "pregunta": "¿Dónde puedo ver los costos de la UTC?",
                "respuesta": "Puedes consultar los costos actualizados de inscripción, colegiaturas y otros servicios en el sitio web oficial de la UTC en la sección de costos: https://utc.edu.mx/costos/. También puedes contactar directamente a Servicios Escolares para información específica.",
                "categoria": "Informacion",
                "keywords": ["costo", "cuota", "precio", "inscripción", "colegiatura", "pago"],
                "link_type": "costos"
            },
            {
                "pregunta": "¿Cuál es la dirección oficial de la UTC?",
                "respuesta": "Para obtener la dirección exacta y detalles de ubicación de la Universidad Tecnológica de Coahuila, puedes consultar la página oficial de contacto: https://utc.edu.mx/contacto/. Ahí encontrarás la dirección completa, mapas y formas de llegar al campus.",
                "categoria": "Informacion",
                "keywords": ["dirección", "ubicación", "donde", "dónde", "lugar", "campus"],
                "link_type": "contacto"
            },
            {
                "pregunta": "¿Cuál es el teléfono de la UTC?",
                "respuesta": "Los números telefónicos oficiales de la Universidad Tecnológica de Coahuila están disponibles en la página de contacto: https://utc.edu.mx/contacto/. Ahí encontrarás teléfonos por departamento y extensiones específicas según tu consulta.",
                "categoria": "Informacion",
                "keywords": ["teléfono", "telefono", "contacto", "llamar", "número"],
                "link_type": "contacto"
            },
            {
                "pregunta": "¿Cuáles son los horarios de atención?",
                "respuesta": "Los horarios de atención de las diferentes áreas administrativas y académicas están publicados en la página oficial: https://utc.edu.mx/contacto/. Te recomiendo revisar esta información ya que pueden variar según el departamento y la época del año.",
                "categoria": "Informacion",
                "keywords": ["horario", "atención", "servicio", "oficina"],
                "link_type": "contacto"
            },
            {
                "pregunta": "¿Cuándo son las inscripciones?",
                "respuesta": "Las fechas de inscripción y convocatorias están disponibles en la sección de admisiones: https://utc.edu.mx/admisiones/. También puedes revisar el calendario académico oficial en: https://utc.edu.mx/calendario/ para todas las fechas importantes del ciclo escolar.",
                "categoria": "Informacion",
                "keywords": ["inscripción", "admisión", "convocatoria", "fechas", "cuando"],
                "link_type": "admisiones"
            },
            {
                "pregunta": "¿Qué carreras ofrece la UTC en detalle?",
                "respuesta": "Puedes consultar toda la información detallada sobre las carreras de TSU e Ingenierías, incluyendo planes de estudio, perfiles de egreso y campos laborales en: https://utc.edu.mx/carreras/. Cada programa tiene su propia sección con información completa.",
                "categoria": "Informacion", 
                "keywords": ["carrera", "programa", "tsu", "ingeniería", "licenciatura", "estudio"],
                "link_type": "carreras"
            },
            {
                "pregunta": "¿Cómo accedo a Mi Portal UTC?",
                "respuesta": "Para acceder a Mi Portal UTC (plataforma de estudiantes), ingresa a: https://mi.utc.edu.mx/. Ahí puedes consultar calificaciones, generar constancias, revisar tu avance académico y realizar diversos trámites en línea.",
                "categoria": "Informacion",
                "keywords": ["mi portal", "plataforma", "calificaciones", "constancia", "trámite"],
                "link_type": "mi_portal"
            },
            {
                "pregunta": "¿Dónde están las noticias oficiales de la UTC?",
                "respuesta": "Las noticias oficiales, comunicados y eventos de la Universidad Tecnológica de Coahuila se publican en: https://utc.edu.mx/noticias/. Ahí encontrarás información actualizada sobre actividades académicas, logros estudiantiles y anuncios importantes.",
                "categoria": "Informacion",
                "keywords": ["noticia", "evento", "comunicado", "información", "anuncio"],
                "link_type": "noticias"
            },
            {
                "pregunta": "¿Cómo contacto a Servicios Escolares?",
                "respuesta": "Para contactar a Servicios Escolares de la UTC, puedes consultar los datos específicos en: https://utc.edu.mx/servicios-escolares/. Ahí encontrarás horarios de atención, teléfonos directos y los trámites que puedes realizar con ellos.",
                "categoria": "Informacion",
                "keywords": ["servicios escolares", "trámite", "documentos", "certificado"],
                "link_type": "servicios_escolares"
            },
            {
                "pregunta": "¿Cuál es el calendario académico actual?",
                "respuesta": "El calendario académico oficial con todas las fechas importantes (inicio de clases, exámenes, vacaciones, etc.) está disponible en: https://utc.edu.mx/calendario/. Se actualiza cada ciclo escolar con las fechas específicas.",
                "categoria": "Calendario",
                "keywords": ["calendario", "fechas", "clases", "examen", "vacaciones"],
                "link_type": "calendario"
            }
        ]
    
    def create_smart_link_responses(self):
        """Crear respuestas inteligentes con enlaces según el contexto"""
        
        link_patterns = {
            "costos_financieros": {
                "triggers": ["costo", "cuota", "precio", "inscripción", "colegiatura", "beca", "financiamiento"],
                "response_template": "Para información actualizada sobre {topic}, te recomiendo consultar:\n\n📍 **Costos oficiales**: https://utc.edu.mx/costos/\n📞 **Servicios Escolares**: https://utc.edu.mx/servicios-escolares/\n🏛️ **Sitio principal**: https://utc.edu.mx/\n\nTambién puedes contactar directamente por teléfono para información personalizada."
            },
            
            "ubicacion_contacto": {
                "triggers": ["dirección", "ubicación", "teléfono", "contacto", "donde", "lugar"],
                "response_template": "Para encontrar la información de contacto y ubicación que necesitas:\n\n📍 **Contacto oficial**: https://utc.edu.mx/contacto/\n🗺️ **Ubicación y mapas**: https://utc.edu.mx/contacto/\n📞 **Teléfonos por departamento**: https://utc.edu.mx/contacto/\n\nEn esta página encontrarás direcciones exactas, números telefónicos y horarios de atención."
            },
            
            "carreras_academico": {
                "triggers": ["carrera", "programa", "tsu", "ingeniería", "licenciatura", "plan de estudios"],
                "response_template": "Para explorar la oferta académica completa de la UTC:\n\n🎓 **Todas las carreras**: https://utc.edu.mx/carreras/\n📚 **Planes de estudio**: https://utc.edu.mx/carreras/\n📝 **Admisiones**: https://utc.edu.mx/admisiones/\n\nCada programa tiene información detallada sobre perfil de egreso, campo laboral y duración."
            },
            
            "tramites_servicios": {
                "triggers": ["trámite", "constancia", "certificado", "documento", "mi portal", "calificaciones"],
                "response_template": "Para realizar trámites y consultar servicios estudiantiles:\n\n🏛️ **Mi Portal UTC**: https://mi.utc.edu.mx/\n📋 **Servicios Escolares**: https://utc.edu.mx/servicios-escolares/\n📞 **Contacto directo**: https://utc.edu.mx/contacto/\n\nEn Mi Portal puedes generar constancias, consultar calificaciones y realizar varios trámites en línea."
            },
            
            "fechas_calendario": {
                "triggers": ["fecha", "cuando", "inscripción", "examen", "calendario", "semestre"],
                "response_template": "Para consultar fechas importantes y calendario académico:\n\n📅 **Calendario oficial**: https://utc.edu.mx/calendario/\n📝 **Convocatorias**: https://utc.edu.mx/admisiones/\n📰 **Noticias y eventos**: https://utc.edu.mx/noticias/\n\nEstas páginas se mantienen actualizadas con todas las fechas relevantes del ciclo escolar."
            }
        }
        
        return link_patterns
    
    def enhance_training_with_links(self):
        """Mejorar los datos de entrenamiento con enlaces oficiales"""
        
        # Cargar datos existentes
        try:
            with open('exported_data/utc_enhanced_training_data.json', 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            print("⚠️ Archivo de entrenamiento previo no encontrado, creando desde cero")
            existing_data = []
        
        # Agregar nuevos datos con enlaces
        enhanced_data = existing_data.copy()
        
        # Agregar datos específicos de enlaces
        for item in self.link_training_data:
            enhanced_data.append({
                **item,
                "enhanced": True,
                "has_official_links": True,
                "training_version": "2.0_with_links",
                "timestamp": datetime.now().isoformat()
            })
        
        # Crear variaciones adicionales con enlaces
        link_variations = [
            {
                "pregunta": "Enlaces oficiales de la UTC",
                "respuesta": """Aquí tienes los enlaces oficiales principales de la Universidad Tecnológica de Coahuila:

🏛️ **Sitio Principal**: https://utc.edu.mx/
👨‍🎓 **Mi Portal Estudiantes**: https://mi.utc.edu.mx/
📚 **Carreras y Programas**: https://utc.edu.mx/carreras/
📝 **Admisiones**: https://utc.edu.mx/admisiones/
📋 **Servicios Escolares**: https://utc.edu.mx/servicios-escolares/
💰 **Costos**: https://utc.edu.mx/costos/
📞 **Contacto**: https://utc.edu.mx/contacto/
📅 **Calendario**: https://utc.edu.mx/calendario/
📰 **Noticias**: https://utc.edu.mx/noticias/

Todos estos enlaces te llevan a información oficial y actualizada de la universidad.""",
                "categoria": "Informacion",
                "enhanced": True,
                "has_official_links": True,
                "priority": "high"
            },
            
            {
                "pregunta": "¿Cómo obtener información oficial de la UTC?",
                "respuesta": """Para obtener información oficial y actualizada de la Universidad Tecnológica de Coahuila, siempre consulta las fuentes oficiales:

🌐 **Sitio web oficial**: https://utc.edu.mx/
📧 **Contacto directo**: https://utc.edu.mx/contacto/
📱 **Redes sociales oficiales**: Disponibles en la página de contacto

Evita información de fuentes no oficiales y siempre verifica que las páginas web tengan el dominio utc.edu.mx para asegurar que sea información oficial de la universidad.""",
                "categoria": "Informacion",
                "enhanced": True,
                "has_official_links": True,
                "priority": "high"
            }
        ]
        
        enhanced_data.extend(link_variations)
        
        # Guardar datos mejorados
        output_file = 'exported_data/utc_enhanced_training_data_v2.json'
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(enhanced_data, file, ensure_ascii=False, indent=2)
        
        print(f"✅ Entrenamiento con enlaces completado")
        print(f"📊 Total de entradas: {len(enhanced_data)}")
        print(f"🔗 Nuevas entradas con enlaces: {len(self.link_training_data) + len(link_variations)}")
        print(f"📁 Guardado en: {output_file}")
        
        return enhanced_data
    
    def create_link_detection_system(self):
        """Sistema para detectar cuándo sugerir enlaces específicos"""
        
        detection_rules = {
            "rule_1": {
                "description": "Detectar consultas de costos",
                "keywords": ["costo", "cuota", "precio", "inscripción", "colegiatura", "cuanto", "pago"],
                "suggested_links": [
                    "https://utc.edu.mx/costos/",
                    "https://utc.edu.mx/servicios-escolares/"
                ],
                "response_type": "costos_financieros"
            },
            
            "rule_2": {
                "description": "Detectar consultas de ubicación/contacto",
                "keywords": ["dirección", "ubicación", "teléfono", "contacto", "donde", "lugar", "horario"],
                "suggested_links": [
                    "https://utc.edu.mx/contacto/"
                ],
                "response_type": "ubicacion_contacto"
            },
            
            "rule_3": {
                "description": "Detectar consultas académicas",
                "keywords": ["carrera", "programa", "tsu", "ingeniería", "licenciatura", "estudiar", "plan"],
                "suggested_links": [
                    "https://utc.edu.mx/carreras/",
                    "https://utc.edu.mx/admisiones/"
                ],
                "response_type": "carreras_academico"
            },
            
            "rule_4": {
                "description": "Detectar consultas de trámites",
                "keywords": ["trámite", "constancia", "certificado", "documento", "portal", "calificaciones"],
                "suggested_links": [
                    "https://mi.utc.edu.mx/",
                    "https://utc.edu.mx/servicios-escolares/"
                ],
                "response_type": "tramites_servicios"
            },
            
            "rule_5": {
                "description": "Detectar consultas de fechas",
                "keywords": ["fecha", "cuando", "calendario", "inscripción", "examen", "semestre"],
                "suggested_links": [
                    "https://utc.edu.mx/calendario/",
                    "https://utc.edu.mx/admisiones/"
                ],
                "response_type": "fechas_calendario"
            }
        }
        
        # Guardar reglas de detección
        with open('exported_data/link_detection_rules.json', 'w', encoding='utf-8') as file:
            json.dump(detection_rules, file, ensure_ascii=False, indent=2)
        
        return detection_rules

def run_links_training():
    """Ejecutar entrenamiento con enlaces oficiales"""
    print("🔗 INICIANDO ENTRENAMIENTO CON ENLACES OFICIALES")
    print("=" * 60)
    
    trainer = UTCOfficialLinksTrainer()
    
    # Mejorar entrenamiento con enlaces
    enhanced_data = trainer.enhance_training_with_links()
    
    # Crear sistema de detección de enlaces
    detection_rules = trainer.create_link_detection_system()
    print("✅ Sistema de detección de enlaces creado")
    
    # Crear patrones de respuesta inteligente
    link_patterns = trainer.create_smart_link_responses()
    
    # Guardar patrones
    with open('exported_data/smart_link_patterns.json', 'w', encoding='utf-8') as file:
        json.dump(link_patterns, file, ensure_ascii=False, indent=2)
    
    print("✅ Patrones de enlaces inteligentes creados")
    
    print(f"\n🎯 ENTRENAMIENTO CON ENLACES COMPLETADO")
    print(f"📈 Base de datos expandida a {len(enhanced_data)} entradas")
    print(f"🔗 {len(trainer.link_training_data)} nuevas respuestas con enlaces oficiales")
    print(f"🎛️ {len(detection_rules)} reglas de detección configuradas")
    
    print("\n💡 Próximos pasos:")
    print("  1. Actualizar el chatbot para usar los nuevos datos")
    print("  2. Implementar detección automática de enlaces")
    print("  3. Probar con consultas sobre costos, ubicación y carreras")
    
    return enhanced_data, detection_rules, link_patterns

if __name__ == "__main__":
    run_links_training()