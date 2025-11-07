"""
Configuración y utilidades para Google Gemini API
Sistema de chatbot inteligente para la Universidad Tecnológica de Coahuila
"""

import os
import json
import google.generativeai as genai
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class GeminiConfig:
    """Configuración centralizada para Google Gemini API"""
    
    # API Configuration
    API_KEY = os.getenv('GEMINI_API_KEY')
    MODEL_NAME = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
    
    # Generation parameters
    TEMPERATURE = float(os.getenv('GEMINI_TEMPERATURE', '0.7'))
    MAX_OUTPUT_TOKENS = int(os.getenv('GEMINI_MAX_TOKENS', '1000'))
    TOP_P = float(os.getenv('GEMINI_TOP_P', '0.95'))
    TOP_K = int(os.getenv('GEMINI_TOP_K', '40'))
    
    # UTC-specific configuration
    UTC_CONTEXT_FILE = os.path.join(os.path.dirname(__file__), 'exported_data', 'utc_training_data_20251105_192821.json')
    UTC_FALLBACK_FILE = os.path.join(os.path.dirname(__file__), 'exported_data', 'utc_training_data_20251105_192821.json')
    UTC_ORIGINAL_FILE = os.path.join(os.path.dirname(__file__), 'exported_data', 'utc_training_data_20251105_192821.json')
    
    # Safety settings
    SAFETY_SETTINGS = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]
    
    @classmethod
    def initialize_gemini(cls):
        """Inicializar la API de Gemini"""
        if not cls.API_KEY or cls.API_KEY == 'tu_gemini_api_key_aqui':
            raise ValueError(
                "❌ GEMINI_API_KEY no configurada. "
                "Por favor:\n"
                "1. Ve a https://makersuite.google.com\n"
                "2. Obtén tu API key gratuita\n"
                "3. Crea un archivo .env con: GEMINI_API_KEY=tu_clave_aqui"
            )
        
        genai.configure(api_key=cls.API_KEY)
        
        # Configurar el modelo
        generation_config = {
            "temperature": cls.TEMPERATURE,
            "top_p": cls.TOP_P,
            "top_k": cls.TOP_K,
            "max_output_tokens": cls.MAX_OUTPUT_TOKENS,
        }
        
        model = genai.GenerativeModel(
            model_name=cls.MODEL_NAME,
            generation_config=generation_config,
            safety_settings=cls.SAFETY_SETTINGS
        )
        
        return model
    
    @classmethod
    def load_utc_context(cls) -> Dict:
        """Cargar el contexto de la UTC desde los datos exportados"""
        try:
            # Intentar cargar datos v2 con enlaces primero
            with open(cls.UTC_CONTEXT_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
            print(f"✅ Datos v2 con enlaces cargados: {len(data)} entradas")
        except FileNotFoundError:
            try:
                # Fallback a datos v1 mejorados
                with open(cls.UTC_FALLBACK_FILE, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                print(f"✅ Datos v1 mejorados cargados: {len(data)} entradas")
            except FileNotFoundError:
                try:
                    # Fallback a datos originales
                    with open(cls.UTC_ORIGINAL_FILE, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                    print(f"✅ Datos originales cargados: {len(data)} entradas")
                except FileNotFoundError:
                    print(f"❌ No se encontraron archivos de contexto")
                    return {'knowledge_base': [], 'categories': {}, 'total_questions': 0}
        
        # Organizar por categorías y detectar características especiales
        context = {
            'total_questions': len(data),
            'categories': {},
            'knowledge_base': data,
            'enhanced_data': any(item.get('enhanced', False) for item in data),
            'has_official_links': any(item.get('has_official_links', False) for item in data),
            'version': 'v2' if any(item.get('training_version', '').startswith('2.0') for item in data) else 'v1'
        }
        
        for item in data:
            categoria = item.get('categoria', 'General')
            if categoria not in context['categories']:
                context['categories'][categoria] = []
            context['categories'][categoria].append({
                'pregunta': item['pregunta'],
                'respuesta': item['respuesta'],
                'enhanced': item.get('enhanced', False),
                'has_links': item.get('has_official_links', False)
            })
        
        if context['has_official_links']:
            print("🔗 Sistema de enlaces oficiales activado")
        
        return context
    
    @classmethod
    def get_system_prompt(cls, utc_context: Dict) -> str:
        """Generar el prompt del sistema con el contexto de la UTC"""
        
        # Crear resumen de categorías
        categories_summary = ""
        for categoria, items in utc_context['categories'].items():
            categories_summary += f"- {categoria}: {len(items)} elementos\n"
        
        system_prompt = f"""
Eres FALCON, el asistente virtual inteligente especializado de la Universidad Tecnológica de Coahuila (UTC).

CAPACIDADES AVANZADAS:
- Acceso a conocimiento especializado sobre la UTC
- Capacidad de búsqueda y análisis de información web actualizada
- Comprensión contextual avanzada sobre educación superior
- Integración de datos locales con información global

CONOCIMIENTO BASE UTC:
Tienes acceso privilegiado a {utc_context['total_questions']} preguntas y respuestas específicas sobre:
{categories_summary}

DATOS OFICIALES UTC (USAR COMO REFERENCIA):
- Rector: Sergio Alberto Guadarrama Cortés (Nueva Rosita, Coahuila, nacido 5 agosto 1965)
- Ubicación: Universidad Tecnológica de Coahuila, México
- Sistema educativo: 2 años TSU + 1 año 8 meses Ingeniería (total 3 años 8 meses)
- Especialidad: Programas técnicos y de ingeniería de alta calidad
- Enfoque: Educación práctica y vinculación con la industria

INSTRUCCIONES DE BÚSQUEDA INTELIGENTE:
1. SIEMPRE busca información actualizada sobre la UTC cuando sea relevante
2. Combina tu base de conocimientos con información web reciente
3. Verifica datos con fuentes oficiales como utc.mx
4. Proporciona información sobre: carreras, admisiones, requisitos, costos, fechas importantes
5. Busca noticias recientes, eventos, cambios en programas académicos
6. Incluye información de contacto y enlaces oficiales cuando sea útil

TIPOS DE INFORMACIÓN QUE PUEDES BUSCAR:
- Carreras y programas académicos actuales
- Procesos de admisión y requisitos
- Costos de matrícula y becas disponibles
- Calendarios académicos y fechas importantes
- Noticias y eventos de la universidad
- Infraestructura y servicios estudiantiles
- Convenios y vinculación empresarial
- Historia y logros de la universidad

FORMATO DE RESPUESTA PROFESIONAL:
- Respuestas informativas y precisas (2-4 oraciones)
- Datos específicos y actualizados cuando estén disponibles
- Enlaces oficiales relevantes
- Sugerencias de contacto directo cuando sea apropiado
- Tono profesional, amigable y confiable

CRITERIO INTELIGENTE:
- Interpreta las preguntas para ofrecer información completa y útil
- Si no tienes información específica, búscala activamente
- Reformula y enriquece la información con tu criterio profesional
- Prioriza información oficial y verificada
- Sugiere alternativas cuando no encuentres datos exactos

EJEMPLO DE RESPUESTA IDEAL:
"La UTC ofrece [X carreras específicas]. Los requisitos de admisión incluyen [datos específicos]. El proceso inicia en [fechas]. Para más información detallada, puedes consultar utc.mx o contactar al teléfono [número oficial]."

NO HACER:
- Usar emojis o prefijos "FALCON:"
- Dar respuestas vagas o genéricas
- Limitar respuestas solo a tu base de datos local
- Responder "no sé" cuando puedes buscar información
"""
        return system_prompt.strip()

# Test de configuración
def test_gemini_config():
    """Función para probar la configuración de Gemini"""
    try:
        print("🔧 Probando configuración de Gemini...")
        
        # Inicializar Gemini
        model = GeminiConfig.initialize_gemini()
        print("✅ Modelo Gemini inicializado correctamente")
        
        # Cargar contexto UTC
        context = GeminiConfig.load_utc_context()
        print(f"✅ Contexto UTC cargado: {context['total_questions']} preguntas")
        
        # Probar una consulta simple
        system_prompt = GeminiConfig.get_system_prompt(context)
        print("✅ Prompt del sistema generado")
        
        # Test básico
        response = model.generate_content("Hola, ¿qué carreras ofrece la UTC?")
        print("✅ Respuesta de prueba generada")
        print(f"📝 Respuesta: {response.text[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

if __name__ == "__main__":
    test_gemini_config()