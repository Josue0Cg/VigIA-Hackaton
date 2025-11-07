"""
Chatbot FALCON para la Universidad Tecnológica de Coahuila
Implementación con Google Gemini API - Sistema inteligente y mejorado
"""

from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from .models import Database
import json
import os
import sys

# Agregar el directorio actual al path para importar módulos locales
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from utc_gemini_chatbot import UTCGeminiChatbot
    GEMINI_AVAILABLE = True
    print("🚀 FALCON con Google Gemini activado")
except ImportError as e:
    print(f"⚠️ Warning: No se pudo importar Gemini chatbot: {e}")
    GEMINI_AVAILABLE = False

# Instancia global del chatbot (se inicializa una vez)
_gemini_chatbot_instance = None

# DICCIONARIO DE PALABRAS Y SINÓNIMOS PARA FALCON
FALCON_DICTIONARY = {
    # Palabras de saludo y cortesía
    'saludos': {
        'hola': ['Hola', '¡Hola!', 'Buenos días', 'Buen día', 'Saludos'],
        'adios': ['Hasta luego', 'Nos vemos', 'Que tengas buen día', 'Adiós'],
        'gracias': ['De nada', 'Con gusto', 'Para eso estoy aquí', 'Es un placer ayudarte']
    },
    
    # Términos académicos
    'academicos': {
        'carrera': ['programa académico', 'especialidad', 'área de estudio', 'disciplina'],
        'estudiante': ['alumno', 'estudiante', 'educando', 'futuro profesionista'],
        'profesor': ['docente', 'maestro', 'catedrático', 'instructor'],
        'universidad': ['institución educativa', 'alma mater', 'centro de estudios', 'casa de estudios']
    },
    
    # Términos específicos UTC
    'utc_terminos': {
        'tsu': ['Técnico Superior Universitario', 'carrera técnica', 'programa TSU'],
        'ingenieria': ['programa de ingeniería', 'carrera de ingeniería', 'especialidad en ingeniería'],
        'rector': ['máxima autoridad', 'director general', 'líder institucional'],
        'coahuila': ['estado de Coahuila', 'territorio coahuilense', 'región noreste de México']
    },
    
    # Palabras de transición y conectores
    'conectores': {
        'ademas': ['además', 'también', 'asimismo', 'por otra parte', 'cabe mencionar'],
        'importante': ['relevante', 'significativo', 'destacable', 'fundamental', 'esencial'],
        'informacion': ['datos', 'detalles', 'información', 'elementos', 'aspectos'],
        'ofrecer': ['brindar', 'proporcionar', 'facilitar', 'poner a disposición']
    },
    
    # Expresiones de FALCON
    'expresiones_falcon': {
        'ayuda': ['puedo ayudarte', 'estoy aquí para asistirte', 'te puedo orientar', 'permíteme apoyarte'],
        'saber_mas': ['conocer más detalles', 'obtener información adicional', 'profundizar en el tema'],
        'contacto': ['comunicarte directamente', 'ponerte en contacto', 'solicitar información específica']
    },
    
    # Palabras técnicas UTC
    'tecnicas': {
        'duracion': ['tiempo de duración', 'período académico', 'años de estudio', 'tiempo requerido'],
        'requisitos': ['condiciones', 'documentos necesarios', 'criterios de ingreso', 'especificaciones'],
        'admision': ['proceso de ingreso', 'inscripción', 'procedimiento de admisión', 'acceso académico']
    }
}

def enrich_text_with_dictionary(text, question_type='general'):
    """Función simplificada - sin diccionario complejo"""
    # Simplemente devolver el texto tal como está para evitar confusión
    return text

def get_contextual_phrase(question, context='general'):
    """Función simplificada - sin frases complejas"""
    # Devolver una frase simple para evitar confusión
    return "Te puedo decir que"

def add_falcon_personality(response, question):
    """Función simplificada - sin personalidad compleja"""
    # Devolver la respuesta tal como está para evitar confusión
    return response
    
    # Enriquecer el texto principal
    enriched_response = enrich_text_with_dictionary(response)
    
    # Agregar frase de cierre ocasionalmente (20% de las veces)
    if random.random() < 0.2 and '?' not in enriched_response:
        enriched_response += f" {random.choice(closing_phrases)}"
    
    return enriched_response

def get_gemini_chatbot():
    """Obtener o crear instancia del chatbot Gemini"""
    global _gemini_chatbot_instance
    
    if _gemini_chatbot_instance is None and GEMINI_AVAILABLE:
        try:
            _gemini_chatbot_instance = UTCGeminiChatbot()
            if not _gemini_chatbot_instance.initialize():
                print("❌ Error: No se pudo inicializar el chatbot Gemini")
                _gemini_chatbot_instance = None
        except Exception as e:
            print(f"❌ Error creando chatbot Gemini: {e}")
            _gemini_chatbot_instance = None
    
    return _gemini_chatbot_instance

def search_direct_database(question):
    """Búsqueda simple en base de datos - solo para casos muy específicos"""
    try:
        print(f"🔍 Búsqueda rápida: '{question}'")
        
        # Solo buscar coincidencias exactas y muy específicas
        question_lower = question.lower()
        
        # Casos específicos que deben ir directo a BD
        specific_cases = {
            'rector': 'Nuestro rector es Sergio Alberto Guadarrama Cortés, nacido el 5 de agosto de 1965 en Nueva Rosita, Coahuila.',
            'hola': '¡Hola! Soy FALCON, tu asistente virtual especializado de la Universidad Tecnológica de Coahuila.',
            'quien eres': 'Soy FALCON, tu asistente virtual especializado de la UTC, diseñado para ayudarte con información sobre programas académicos, trámites y servicios universitarios.',
        }
        
        # Buscar coincidencia directa
        for key, response in specific_cases.items():
            if key in question_lower:
                print(f"✅ Coincidencia directa encontrada: {key}")
                return {
                    'found': True,
                    'response': response,
                    'title': 'FALCON - Asistente Virtual UTC',
                    'confidence_score': 95,
                    'source': 'direct_match'
                }
        
        # Para todo lo demás, dejar que Gemini maneje la respuesta
        print("� Enviando a Gemini para mejor comprensión...")
        return {
            'found': False,
            'reason': 'Enviando a Gemini para respuesta inteligente'
        }
        
        # No se encontró respuesta directa
        return {'found': False, 'reason': 'No match found in database'}
        
    except Exception as e:
        print(f"❌ Error en búsqueda directa: {e}")
        return {'found': False, 'reason': f'Error: {e}'}

def find_best_match_in_training_data(question, training_data):
    """Encontrar la mejor coincidencia en datos entrenados con lógica contextual mejorada"""
    question_lower = question.lower()
    best_match = None
    best_score = 0
    
    # Palabras clave de la pregunta (filtrar palabras muy cortas)
    question_words = [w.strip() for w in question_lower.split() if len(w) > 2]
    
    # Patrones de preguntas específicas para mejor coincidencia
    question_patterns = {
        # Preguntas sobre qué hace FALCON (el asistente)
        'falcon_funciones': ['que hace la ia', 'que haces', 'para que sirves', 'que funciones tienes', 'como me ayudas'],
        # Preguntas sobre carreras de IA (el programa académico)
        'carrera_ia': ['carrera de inteligencia artificial', 'carrera de ia', 'estudiar ia', 'programa de ia'],
        # Preguntas generales sobre carreras
        'carreras_generales': ['que carreras tienen', 'cuales carreras', 'programas academicos', 'que puedo estudiar'],
        # Preguntas sobre FALCON como entidad
        'falcon_identidad': ['que eres', 'quien eres', 'eres un asistente'],
        # Preguntas sobre costos
        'costos': ['cuanto cuesta', 'precio', 'costo', 'cuota'],
        # Preguntas sobre rector
        'rector': ['rector', 'director', 'quien dirige'],
        # Preguntas sobre ubicación
        'ubicacion': ['donde esta', 'ubicacion', 'direccion']
    }
    
    # Identificar el tipo de pregunta
    question_type = None
    for pattern_name, keywords in question_patterns.items():
        if any(keyword in question_lower for keyword in keywords):
            question_type = pattern_name
            break
    
    for item in training_data:
        score = 0
        pregunta_lower = item['pregunta'].lower()
        respuesta_lower = item['respuesta'].lower()
        
        # Si identificamos el tipo de pregunta, priorizar respuestas relacionadas
        if question_type:
            if question_type == 'falcon_funciones':
                # Para "qué hace la IA", buscar respuestas sobre funciones de FALCON
                if any(word in pregunta_lower for word in ['que hace', 'funciones', 'para que sirve', 'asistente']):
                    score += 30  # Alta prioridad para funciones de FALCON
                # Penalizar respuestas sobre carreras cuando preguntan funciones
                if any(word in respuesta_lower for word in ['carrera', 'programa academico', 'tsu', 'ingenieria']):
                    score -= 15
            elif question_type == 'carrera_ia':
                # Para preguntas sobre carrera de IA
                if any(word in pregunta_lower for word in ['carrera', 'inteligencia artificial']):
                    score += 30
            elif question_type == 'carreras_generales':
                if any(word in pregunta_lower for word in ['carrera', 'programa', 'estudiar']):
                    score += 25
            elif question_type == 'falcon_identidad':
                if any(word in pregunta_lower for word in ['asistente', 'falcon', 'que eres']):
                    score += 30
            elif question_type == 'costos' and any(word in pregunta_lower for word in ['costo', 'precio']):
                score += 25
            elif question_type == 'rector' and 'rector' in pregunta_lower:
                score += 25
            elif question_type == 'ubicacion' and any(word in pregunta_lower for word in ['donde', 'ubicacion']):
                score += 25
        
        # Coincidencia exacta o muy alta
        if question_lower.strip() == pregunta_lower.strip():
            score += 30
        elif any(phrase in pregunta_lower for phrase in question_lower.split() if len(phrase) > 4):
            score += 15
        
        # Palabras clave importantes (solo si no hay coincidencia de patrón)
        if score < 20:
            for word in question_words:
                if word in pregunta_lower:
                    score += 10  # Alta puntuación para pregunta
                elif word in respuesta_lower:
                    score += 2   # Muy baja puntuación para respuesta
        
        # Penalización por respuestas que no coinciden con el contexto
        if question_type == 'que_hace_ia':
            if any(word in respuesta_lower for word in ['carrera', 'programa academico', 'tsu']):
                score -= 10  # Penalizar respuestas sobre carreras cuando preguntan qué hace
        
        # Coincidencias especiales específicas
        special_matches = {
            'rector': ['rector', 'director', 'quien dirige'],
            'carrera': ['carrera', 'programa', 'estudiar', 'licenciatura', 'ingenieria'],
            'costo': ['costo', 'precio', 'cuanto cuesta', 'cuota', 'pagar'],
            'ubicacion': ['donde', 'ubicacion', 'direccion', 'lugar'],
            'admision': ['admision', 'inscripcion', 'requisito', 'ingreso'],
            'duracion': ['duracion', 'cuanto tiempo', 'años', 'semestre']
        }
        
        for tema, keywords in special_matches.items():
            if any(kw in question_lower for kw in keywords) and any(kw in pregunta_lower for kw in keywords):
                score += 15
        
        if score > best_score and score > 5:  # Umbral mínimo
            best_score = score
            best_match = {**item, 'score': score}
    
    if best_match and best_score > 8:  # Umbral de confianza
        print(f"✅ Coincidencia encontrada: {best_match['pregunta'][:50]}... (puntuación: {best_score})")
        
        # PERSONALIZAR la respuesta basándose en la información de la BD
        personalized_response = personalize_response(question, best_match, question_lower)
        best_match['respuesta_personalizada'] = personalized_response
        
        return best_match
    
    return None

def personalize_response(question, match_data, question_lower):
    """Personalizar respuesta basándose en la información de la BD pero con palabras propias de FALCON"""
    original_response = match_data['respuesta']
    categoria = match_data.get('categoria', 'General')
    
    # Limpiar respuesta original de referencias a otros bots
    cleaned_response = original_response.replace('Hawky', 'FALCON')
    cleaned_response = cleaned_response.replace('hawky', 'FALCON')
    cleaned_response = cleaned_response.replace('howki', 'FALCON')
    cleaned_response = cleaned_response.replace('Hola, soy', 'Soy FALCON,')
    cleaned_response = cleaned_response.replace('Eres un asistente', 'Soy FALCON, un asistente avanzado')
    
    # Personalización inteligente por categoría y tipo de pregunta
    if 'rector' in question_lower:
        if 'sergio' in cleaned_response.lower() or 'guadarrama' in cleaned_response.lower():
            enhanced_response = f"Te comento que nuestro rector es Sergio Alberto Guadarrama Cortés. Nació el 5 de agosto de 1965 en Nueva Rosita, Coahuila, y ha liderado fundamentals iniciativas de modernización en nuestra institución universitaria."
            return enrich_text_with_dictionary(enhanced_response, 'utc_terminos')
    
    elif any(word in question_lower for word in ['carrera', 'programa', 'estudiar', 'licenciatura', 'ia', 'inteligencia', 'artificial']):
        # Respuesta especial para IA
        if any(ia_word in question_lower for ia_word in ['ia', 'inteligencia', 'artificial', 'machine', 'learning']):
            enhanced_response = f"¡Excelente pregunta! Nuestra institución ahora cuenta con la innovadora carrera de Inteligencia Artificial. Este programa de vanguardia te forma en tecnologías emergentes como machine learning, deep learning y robótica inteligente. Ofrecemos tanto la modalidad TSU (2 años) como Ingeniería (3 años 8 meses), con laboratorios especializados de última generación."
            return enrich_text_with_dictionary(enhanced_response, 'academicos')
        elif 'tsu' in cleaned_response.lower() or 'ingeniería' in cleaned_response.lower():
            enhanced_response = f"Te puedo decir que ofrecemos una amplia variedad de programas académicos innovadores. Nuestro sistema educativo incluye especialidades de Técnico Superior Universitario (TSU) de 2 años y programas de Ingeniería que suman 3 años y 8 meses en total. Contamos con especialidades en áreas tecnológicas avanzadas, incluyendo nuestra nueva carrera de Inteligencia Artificial, todas diseñadas para formar profesionales altamente capacitados para la industria 4.0."
            return enrich_text_with_dictionary(enhanced_response, 'academicos')
    
    elif any(word in question_lower for word in ['duración', 'tiempo', 'cuanto dura']):
        if '3' in cleaned_response or 'años' in cleaned_response.lower():
            enhanced_response = f"Nuestro sistema educativo está estructurado en etapas: primero cursas 2 años para obtener tu título de Técnico Superior Universitario (TSU), y luego puedes continuar 1 año y 8 meses adicionales para completar tu Ingeniería. En total son 3 años y 8 meses para la carrera completa."
            return enrich_text_with_dictionary(enhanced_response, 'academicos')
    
    elif any(word in question_lower for word in ['ubicación', 'donde', 'dirección']):
        if 'coahuila' in cleaned_response.lower():
            enhanced_response = f"Nos encontramos ubicados en el estado de Coahuila, México. Somos una institución comprometida con la excelencia académica y la formación integral de nuestros estudiantes."
            return enrich_text_with_dictionary(enhanced_response, 'utc_terminos')
    
    elif any(word in question_lower for word in ['costo', 'precio', 'cuota', 'pagar']):
        enhanced_response = f"Para información actualizada sobre costos y cuotas, te recomiendo contactar directamente con nosotros, ya que pueden variar según el programa y tenemos diferentes opciones de becas disponibles. Puedes obtener detalles específicos en nuestra oficina de administración escolar."
        return enrich_text_with_dictionary(enhanced_response, 'tecnicas')
    
    elif 'hola' in question_lower or 'saludo' in question_lower or any(word in question_lower for word in ['asistente', 'que eres', 'quien eres']):
        base_greeting = f"¡{get_contextual_phrase(question, 'saludos')}! Soy FALCON, tu asistente virtual especializado de la Universidad Tecnológica de Coahuila. Estoy diseñado con inteligencia artificial avanzada para brindarte información actualizada sobre nuestros programas académicos innovadores, incluyendo nuestra nueva carrera de Inteligencia Artificial, trámites administrativos, admisiones y todo lo relacionado con nuestra institución educativa. ¿En qué aspectos puedo asistirte hoy?"
        return enrich_text_with_dictionary(base_greeting, 'expresiones_falcon')
    
    # Personalización avanzada para respuestas generales
    else:
        # Convertir de tercera persona a respuesta directa y natural
        cleaned_response = cleaned_response.replace('La UTC tiene', 'Nuestra institución cuenta con')
        cleaned_response = cleaned_response.replace('La UTC ofrece', 'Te puedo decir que ofrecemos')
        cleaned_response = cleaned_response.replace('La UTC cuenta con', 'Contamos con')
        cleaned_response = cleaned_response.replace('La universidad tiene', 'Nuestra casa de estudios tiene')
        cleaned_response = cleaned_response.replace('La universidad ofrece', 'Brindamos')
        cleaned_response = cleaned_response.replace('La universidad cuenta', 'Contamos')
        cleaned_response = cleaned_response.replace('universidad tecnologica de coahuila llamada howki', 'FALCON, asistente especializado de la UTC')
        
        # Enriquecer con diccionario antes de personalizar
        enriched_response = enrich_text_with_dictionary(cleaned_response, 'utc_terminos')
        
        # Agregar introducción natural y contextual
        if len(enriched_response) > 80 and not any(start in enriched_response[:25].lower() for start in ['tenemos', 'ofrecemos', 'contamos', 'nuestro', 'te puedo', 'con gusto']):
            connector = get_contextual_phrase(question, 'conectores')
            enriched_response = f"{connector} {enriched_response}"
        
        # Hacer la respuesta más conversacional
        if 'destinada a poder ayudar' in enriched_response:
            enriched_response = enriched_response.replace('destinada a poder ayudar a los usuarios de cualquier forma posible y que tengas conocimiento sobre ello', 'especializado en brindarte información precisa y actualizada sobre todos los aspectos de nuestra universidad')
        
        
        # Agregar personalidad FALCON
        final_response = add_falcon_personality(enriched_response, question)
        
        # Limpiar y mejorar formato
        final_response = final_response.replace('  ', ' ')
        final_response = final_response.strip()
        
        return final_response
    
    # Fallback - devolver respuesta enriquecida
    return enrich_text_with_dictionary(cleaned_response, 'general')

def find_best_match_in_django_db(question):
    """Buscar en base de datos Django como respaldo"""
    try:
        results = Database.objects.filter(
            informacion__isnull=False
        ).exclude(informacion='')
        
        question_lower = question.lower()
        question_words = [w for w in question_lower.split() if len(w) > 2]
        
        best_match = None
        best_score = 0
        
        for result in results:
            score = 0
            title_lower = result.titulo.lower()
            info_lower = result.informacion.lower()
            
            # Coincidencia directa en título o información
            if any(word in title_lower for word in question_words):
                score += 5
            if any(word in info_lower for word in question_words):
                score += 2
            
            if score > best_score and score > 3:
                best_score = score
                best_match = result
        
        if best_match:
            print(f"✅ Encontrado en Django DB: {best_match.titulo}")
            
            # Personalizar respuesta de Django DB también
            personalized_django_response = personalize_django_response(question, best_match)
            
            return {
                'found': True,
                'response': personalized_django_response,
                'title': 'FALCON - Asistente Virtual UTC',
                'redirect': best_match.redirigir,
                'image': best_match.imagen.url if best_match.imagen else None,
                'confidence_score': best_score,
                'source': 'django_database_personalized'
            }
        
        return None
        
    except Exception as e:
        print(f"❌ Error en búsqueda Django: {e}")
        return None

def personalize_django_response(question, django_match):
    """Personalizar respuestas de Django DB como FALCON"""
    original_info = django_match.informacion
    question_lower = question.lower()
    
    # Limpiar respuesta de referencias a otros bots
    personalized = original_info.replace('Hawky', 'FALCON')
    personalized = personalized.replace('hawky', 'FALCON')
    personalized = personalized.replace('Hola, soy', 'Soy FALCON,')
    
    # Reformular según el tipo de pregunta (sin tercera persona)
    if 'rector' in question_lower:
        personalized = f"Nuestro rector es {personalized.replace('El rector es', '').strip()}."
    
    elif any(word in question_lower for word in ['carrera', 'programa', 'estudiar']):
        if 'ofrece' not in personalized.lower():
            personalized = f"Tenemos {personalized.lower()}"
        else:
            personalized = personalized.replace('La UTC ofrece', 'Ofrecemos')
            personalized = personalized.replace('ofrece', 'ofrecemos')
    
    elif any(word in question_lower for word in ['ceremonia', 'graduación', 'titulación']):
        personalized = f"Sobre nuestras ceremonias de graduación: {personalized}"
    
    elif 'hola' in question_lower:
        personalized = f"¡Hola! Soy FALCON, tu asistente virtual de la UTC. {personalized}"
    
    # Asegurar que no empiece con mayúscula suelta
    if len(personalized) > 1 and personalized[0].isupper() and personalized[1].islower():
        personalized = personalized[0].lower() + personalized[1:]
    
    # Agregar punto final si no lo tiene
    if personalized and not personalized.endswith('.') and not personalized.endswith('!') and not personalized.endswith('?'):
        personalized += '.'
    
    return personalized

def fallback_chatbot(question):
    """FALCON - Chatbot entrenado usando la base de datos mejorada"""
    try:
        # Cargar datos entrenados de FALCON
        enhanced_data_file = os.path.join(os.path.dirname(__file__), '..', 'exported_data', 'utc_enhanced_training_data.json')
        training_data = []
        
        if os.path.exists(enhanced_data_file):
            with open(enhanced_data_file, 'r', encoding='utf-8') as f:
                training_data = json.load(f)
            print(f"✅ FALCON cargó {len(training_data)} datos entrenados")
        else:
            print("⚠️ Datos entrenados no encontrados, usando base de datos Django")
            
        # Buscar en datos entrenados primero
        if training_data:
            question_lower = question.lower()
            best_match = None
            best_score = 0
            
            for item in training_data:
                score = 0
                pregunta_lower = item['pregunta'].lower()
                respuesta_lower = item['respuesta'].lower()
                
                # Búsqueda inteligente por palabras clave
                question_words = [w for w in question_lower.split() if len(w) > 2]
                
                for word in question_words:
                    if word in pregunta_lower:
                        score += 5  # Alta puntuación para coincidencia en pregunta
                    if word in respuesta_lower:
                        score += 2  # Menor puntuación para respuesta
                
                # Coincidencias exactas especiales
                if "rector" in question_lower and "rector" in pregunta_lower:
                    score += 10
                if "carrera" in question_lower and ("carrera" in pregunta_lower or "programa" in pregunta_lower):
                    score += 8
                if "ceremonia" in question_lower and "ceremonia" in pregunta_lower:
                    score += 8
                
                if score > best_score:
                    best_score = score
                    best_match = item
            
            if best_match and best_score > 3:
                return {
                    "blank": True,
                    "informacion": best_match['respuesta'],
                    "titulo": "FALCON - Asistente Virtual UTC",
                    "redirigir": "",
                    "imagenes": None,
                    "falcon_trained": True,
                    "confidence_score": best_score
                }
        
        # Fallback a base de datos Django
        results = Database.objects.filter(
            informacion__isnull=False
        ).exclude(informacion='')
        
        # Búsqueda simple por palabras clave
        question_words = question.lower().split()
        best_match = None
        best_score = 0
        
        for result in results:
            score = 0
            title_lower = result.titulo.lower()
            info_lower = result.informacion.lower()
            
            # Contar coincidencias en título (peso mayor)
            for word in question_words:
                if len(word) > 2:  # Ignorar palabras muy cortas
                    if word in title_lower:
                        score += 3
                    if word in info_lower:
                        score += 1
            
            if score > best_score:
                best_score = score
                best_match = result
        
        if best_match and best_score > 0:
            # Crear una respuesta más natural
            if "rector" in question.lower():
                natural_response = f"El rector actual de la Universidad Tecnológica de Coahuila es {best_match.informacion.replace('El rector es', '').strip()}."
            elif "carrera" in question.lower() or "programa" in question.lower():
                natural_response = f"La UTC ofrece diversos programas académicos. {best_match.informacion}"
            elif "ceremonia" in question.lower() or "graduación" in question.lower():
                natural_response = f"Sobre las ceremonias de graduación: {best_match.informacion}"
            else:
                natural_response = best_match.informacion
            
            return {
                "blank": True,
                "informacion": natural_response,
                "titulo": best_match.titulo,
                "redirigir": best_match.redirigir,
                "imagenes": best_match.imagen.url if best_match.imagen else None
            }
        else:
            return {
                "informacion": "Lo siento, no encontré información específica sobre tu consulta. Te recomiendo visitar nuestra sección de preguntas frecuentes o contactar directamente a la universidad para obtener información más detallada.",
                "redirigir": "preguntas_frecuentes/",
                "blank": False,
            }
    
    except Exception as e:
        print(f"Error en fallback chatbot: {e}")
        return {
            "informacion": "Disculpa, estoy experimentando dificultades técnicas en este momento. Por favor, intenta de nuevo más tarde o contacta directamente a la universidad.",
            "redirigir": "",
            "blank": False,
        }
def chatbot(request):
    """Vista principal del chatbot - Principalmente Gemini con casos específicos en BD"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '').strip()
            
            if not question:
                return JsonResponse({
                    'success': False, 
                    'message': 'Por favor, escribe tu pregunta 😊'
                })
            
            print(f"📝 Pregunta recibida: {question}")
            
            # PASO 1: Solo casos muy específicos van a BD
            database_result = search_direct_database(question)
            
            if database_result['found']:
                print(f"✅ Respuesta específica encontrada: {database_result['source']}")
                respuesta = {
                    "blank": True,
                    "informacion": database_result['response'],
                    "titulo": "FALCON - Asistente Virtual UTC",
                    "redirigir": "",
                    "imagenes": None
                }
                return JsonResponse({'success': True, 'answer': respuesta})
            
            # PASO 2: Usar Gemini para TODAS las demás preguntas (mejor comprensión)
            print("🤖 Usando Gemini para respuesta inteligente...")
            gemini_bot = get_gemini_chatbot()
            
            if gemini_bot:
                try:
                    result = gemini_bot.generate_response(question)
                    
                    if result['success']:
                        # Asegurar que la respuesta sea de FALCON
                        clean_response = result['response']
                        
                        # Limpiar prefijos repetitivos
                        prefixes_to_remove = [
                            "🤖 FALCON:", "FALCON:", "🤖", "🦅"
                        ]
                        
                        for prefix in prefixes_to_remove:
                            if clean_response.startswith(prefix):
                                clean_response = clean_response[len(prefix):].strip()
                        
                        # Remover emojis al inicio
                        while clean_response and clean_response[0] in "🤖🦅🔍📚💡✅":
                            clean_response = clean_response[1:].strip()
                        
                        # Log de conversación para entrenamiento
                        try:
                            from utc_advanced_trainer import UTCChatbotTrainer
                            trainer = UTCChatbotTrainer()
                            trainer.log_conversation(
                                question=question,
                                response=clean_response,
                                context_used=result.get('relevant_context_count', 0)
                            )
                        except Exception as e:
                            print(f"⚠️ Error logging conversation: {e}")
                        
                        # Asegurar que la respuesta sea como FALCON y no en tercera persona
                        # Convertir tercera persona a primera persona
                        clean_response = clean_response.replace('La UTC tiene', 'Tenemos')
                        clean_response = clean_response.replace('La UTC ofrece', 'Ofrecemos') 
                        clean_response = clean_response.replace('La UTC cuenta con', 'Contamos con')
                        clean_response = clean_response.replace('La universidad tiene', 'Tenemos')
                        clean_response = clean_response.replace('La universidad ofrece', 'Ofrecemos')
                        clean_response = clean_response.replace('La universidad cuenta', 'Contamos')
                        
                        if not any(name in clean_response for name in ['FALCON', 'Soy FALCON', 'como FALCON']):
                            if len(clean_response) > 20:
                                clean_response = f"Como tu asistente de la UTC, {clean_response.lower()}"
                        
                        respuesta = {
                            "blank": True,
                            "informacion": clean_response,
                            "titulo": "FALCON - Asistente Virtual UTC",
                            "redirigir": "",
                            "imagenes": None,
                            "source": "gemini_ai_as_falcon",
                            "web_enhanced": result.get('web_enhanced', False),
                            "context_items": result.get('relevant_context_count', 0)
                        }
                        
                        print(f"✅ Respuesta Gemini generada (contexto: {result.get('relevant_context_count', 0)} items)")
                        return JsonResponse({'success': True, 'answer': respuesta})
                    
                    else:
                        print(f"⚠️ Error en Gemini: {result.get('error', 'Unknown')}")
                
                except Exception as e:
                    print(f"⚠️ Excepción en Gemini: {e}")
            
            # PASO 3: Fallback final con respuesta genérica
            print("🔄 Usando respuesta genérica de fallback...")
            respuesta = {
                "informacion": "Lo siento, no encontré información específica sobre tu consulta. Te recomiendo visitar la página oficial de la UTC o contactar directamente a la universidad para obtener información detallada.",
                "redirigir": "https://www.utc.mx",
                "blank": False,
                "source": "fallback"
            }
            
            return JsonResponse({'success': True, 'answer': respuesta})
    
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False, 
                'message': 'Error en el formato de datos. Intenta de nuevo.'
            })
        except Exception as e:
            print(f"❌ Error inesperado en chatbot: {e}")
            return JsonResponse({
                'success': False, 
                'message': 'Ocurrió un error inesperado. Por favor, intenta de nuevo.'
            })
    
    return JsonResponse({
        'success': False, 
        'message': 'Método no permitido.'
    }, status=405)

def modelsettings(request):
    """Configuración del modelo 3D (compatibilidad)"""
    if request.method == 'POST':
        try:
            from .views import obtener_configuraciones
            quest_id = request.POST.get('idSetings', '1')
            hawkySettings = obtener_configuraciones(quest_id)
            
            # Configuración por defecto para FALCON
            default_config = {
                "model": "hawky.glb",
                "animation": "idle",
                "autoplay": True,
                "camera_orbit": "0deg 75deg 4m",
                "environment_image": "neutral",
                "exposure": "1"
            }
            
            try:
                modelData = hawkySettings.get(f'redes_sociales_{quest_id}', '{}')
                if modelData and modelData != '{}':
                    parsed_data = json.loads(modelData)
                else:
                    parsed_data = default_config
            except (json.JSONDecodeError, KeyError):
                parsed_data = default_config
                
            return JsonResponse(parsed_data, status=200)
            
        except Exception as e:
            print(f"⚠️ Error en modelsettings: {e}")
            return JsonResponse({
                'success': False, 
                'message': f'Configuración no encontrada: {e}'
            }, status=404)
    
    return JsonResponse({
        'success': False, 
        'message': 'Método no permitido.'
    }, status=405)