"""
Chatbot Gemini para la Universidad Tecnológica de Coahuila
Sistema inteligente de respuestas automáticas usando Google Gemini API
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import google.generativeai as genai
from gemini_config import GeminiConfig

# Importar el sistema de búsqueda web
try:
    from utc_web_searcher import UTCWebSearcher
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    print("⚠️ Sistema de búsqueda web no disponible")
    WEB_SEARCH_AVAILABLE = False

# Importar sistema de enlaces inteligentes
try:
    import json
    LINKS_SYSTEM_AVAILABLE = True
except ImportError:
    print("⚠️ Sistema de enlaces no disponible")
    LINKS_SYSTEM_AVAILABLE = False

class UTCGeminiChatbot:
    """
    Chatbot inteligente para la UTC usando Google Gemini API
    """
    
    def __init__(self):
        self.config = GeminiConfig()
        self.model = None
        self.utc_context = None
        self.conversation_history = []
        self.web_searcher = UTCWebSearcher() if WEB_SEARCH_AVAILABLE else None
        
        # Sistema de enlaces inteligentes
        self.links_system = self.load_links_system() if LINKS_SYSTEM_AVAILABLE else None
        
        self.session_stats = {
            'questions_asked': 0,
            'successful_responses': 0,
            'failed_responses': 0,
            'web_searches_used': 0,
            'links_suggested': 0,
            'session_start': datetime.now()
        }
        
    def initialize(self) -> bool:
        """Inicializar el chatbot"""
        try:
            print("🤖 Inicializando Chatbot FALCON para UTC...")
            
            # Inicializar modelo Gemini
            self.model = self.config.initialize_gemini()
            print("✅ Modelo Gemini inicializado")
            
            # Cargar contexto UTC
            self.utc_context = self.config.load_utc_context()
            print(f"✅ Base de conocimientos cargada: {self.utc_context['total_questions']} preguntas")
            
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando chatbot: {e}")
            return False
    
    def preprocess_question(self, question: str) -> str:
        """Preprocesar la pregunta del usuario"""
        # Limpiar y normalizar la pregunta
        question = question.strip()
        
        # Expandir abreviaciones comunes
        replacements = {
            'utc': 'Universidad Tecnológica de Coahuila',
            'tsu': 'Técnico Superior Universitario',
            'lic': 'Licenciatura',
            'ing': 'Ingeniería',
            'ing.': 'Ingeniería',
            'carreras': 'programas académicos',
            'q': 'que',
            'xq': 'porque',
            'x': 'por'
        }
        
        question_lower = question.lower()
        for abbrev, full in replacements.items():
            question_lower = question_lower.replace(abbrev, full)
        
        return question_lower
    
    def find_direct_links_in_database(self, question: str) -> Dict:
        """Buscar enlaces directos en la base de datos"""
        question_lower = question.lower()
        
        # Palabras clave que indican búsqueda de enlaces
        link_keywords = ['link', 'enlace', 'página', 'sitio', 'web', 'url']
        wants_link = any(keyword in question_lower for keyword in link_keywords)
        
        found_links = []
        
        # Buscar entradas que contengan enlaces directos
        for item in self.utc_context['knowledge_base']:
            # Si tiene enlace oficial definido
            if item.get('enlace_oficial'):
                pregunta = item.get('pregunta', '').lower()
                
                # Si la pregunta del usuario coincide con entradas que tienen enlaces
                relevance = 0
                
                # Coincidencias directas
                if any(word in pregunta for word in question_lower.split() if len(word) > 2):
                    relevance += 1
                
                # Si busca enlaces específicamente y esta entrada los tiene
                if wants_link and any(keyword in pregunta for keyword in link_keywords):
                    relevance += 3
                
                # Categorías específicas
                if 'carrera' in question_lower and 'carrera' in pregunta:
                    relevance += 2
                elif 'admisio' in question_lower and 'admisio' in pregunta:
                    relevance += 2
                elif 'contacto' in question_lower and 'contacto' in pregunta:
                    relevance += 2
                elif 'sitio' in question_lower or 'página' in question_lower:
                    relevance += 2
                
                if relevance > 0:
                    found_links.append({
                        'pregunta': item.get('pregunta'),
                        'respuesta': item.get('respuesta'),
                        'enlace': item.get('enlace_oficial'),
                        'tipo': item.get('tipo_enlace', 'general'),
                        'relevance': relevance
                    })
        
        # Ordenar por relevancia
        found_links.sort(key=lambda x: x['relevance'], reverse=True)
        
        return {
            'found_links': found_links[:3],  # Máximo 3 enlaces más relevantes
            'has_direct_links': len(found_links) > 0,
            'wants_link': wants_link
        }

    def find_relevant_context(self, question: str) -> List[Dict]:
        """Encontrar contexto relevante en la base de conocimientos"""
        question_processed = self.preprocess_question(question)
        relevant_items = []
        
        # Expandir búsqueda con sinónimos y palabras clave específicas
        synonyms = {
            'rector': ['rector', 'director', 'guadarrama', 'sergio', 'alberto'],
            'carrera': ['carrera', 'programa', 'licenciatura', 'ingeniería', 'tsu'],
            'costo': ['costo', 'precio', 'cuota', 'pago', 'inscripción'],
            'graduación': ['graduación', 'ceremonia', 'titulación', 'egreso'],
            'ubicación': ['ubicación', 'dirección', 'donde', 'dónde', 'lugar']
        }
        
        # Expandir palabras de búsqueda
        search_words = set(question_processed.split())
        for key, values in synonyms.items():
            if any(word in question_processed for word in values):
                search_words.update(values)
        
        # Buscar coincidencias exactas y similares
        for item in self.utc_context['knowledge_base']:
            titulo = item['pregunta'].lower()
            respuesta = item['respuesta'].lower()
            
            # Calcular relevancia
            relevance_score = 0
            
            # Buscar coincidencias directas
            for word in search_words:
                if len(word) > 2:  # Ignorar palabras muy cortas
                    # Coincidencias en título (peso alto)
                    if word in titulo:
                        relevance_score += 5
                    # Coincidencias en respuesta (peso medio)
                    if word in respuesta:
                        relevance_score += 2
            
            # Coincidencias de frases específicas (peso muy alto)
            if any(phrase in titulo or phrase in respuesta for phrase in ['sergio alberto', 'guadarrama', 'rector']):
                relevance_score += 15
            
            if relevance_score > 0:
                item_copy = item.copy()
                item_copy['relevance_score'] = relevance_score
                relevant_items.append(item_copy)
        
        # Ordenar por relevancia y retornar los más relevantes
        relevant_items.sort(key=lambda x: x['relevance_score'], reverse=True)
        return relevant_items[:5]  # Top 5 más relevantes
    
    def should_use_web_search(self, question: str, relevant_context: List[Dict]) -> bool:
        """Determinar si se debe usar búsqueda web"""
        if not self.web_searcher:
            return False
        
        # Palabras clave que siempre requieren búsqueda web actualizada
        always_web_keywords = [
            'costo', 'cuota', 'precio', 'ubicación', 'dirección', 'teléfono',
            'contacto', 'horario', 'evento', 'fecha', 'admisión', 'requisito',
            'cuanto cuesta', 'donde esta', 'telefono', 'direccion'
        ]
        
        question_lower = question.lower()
        
        # Siempre usar web search para estas preguntas específicas
        if any(keyword in question_lower for keyword in always_web_keywords):
            print(f"🌐 Activando búsqueda web para: {question}")
            return True
        
        # Usar búsqueda web si hay muy poco contexto relevante
        if len(relevant_context) <= 1:
            print(f"🌐 Poco contexto ({len(relevant_context)} items), activando búsqueda web")
            return True
        
        # Verificar si las respuestas del contexto parecen incompletas
        if len(relevant_context) > 0:
            context_text = " ".join([item['respuesta'].lower() for item in relevant_context])
            incomplete_indicators = [
                'no tengo información', 'no cuento con', 'contacta', 'visita',
                'información actualizada', 'más detalles'
            ]
            
            if any(indicator in context_text for indicator in incomplete_indicators):
                print(f"🌐 Contexto incompleto detectado, activando búsqueda web")
                return True
        
        return False
    
    def load_links_system(self) -> Dict:
        """Cargar sistema de enlaces inteligentes"""
        try:
            with open('exported_data/link_detection_rules.json', 'r', encoding='utf-8') as file:
                detection_rules = json.load(file)
            
            with open('exported_data/smart_link_patterns.json', 'r', encoding='utf-8') as file:
                link_patterns = json.load(file)
            
            return {
                'detection_rules': detection_rules,
                'link_patterns': link_patterns,
                'enabled': True
            }
        except FileNotFoundError:
            print("⚠️ Archivos del sistema de enlaces no encontrados")
            return {'enabled': False}
    
    def detect_link_needs(self, question: str) -> Dict:
        """Detectar si la pregunta necesita enlaces oficiales"""
        if not self.links_system or not self.links_system.get('enabled', False):
            return {'needs_links': False}
        
        question_lower = question.lower()
        detected_rules = []
        
        for rule_id, rule in self.links_system['detection_rules'].items():
            if any(keyword in question_lower for keyword in rule['keywords']):
                detected_rules.append({
                    'rule_id': rule_id,
                    'description': rule['description'],
                    'response_type': rule['response_type'],
                    'suggested_links': rule['suggested_links']
                })
        
        return {
            'needs_links': len(detected_rules) > 0,
            'detected_rules': detected_rules,
            'primary_type': detected_rules[0]['response_type'] if detected_rules else None
        }
    
    def enhance_response_with_links(self, question: str, base_response: str, link_detection: Dict) -> str:
        """Mejorar respuesta agregando enlaces oficiales relevantes"""
        if not link_detection['needs_links']:
            return base_response
        
        try:
            self.session_stats['links_suggested'] += 1
            primary_type = link_detection['primary_type']
            
            # Obtener patrón de enlaces para el tipo detectado
            if primary_type in self.links_system['link_patterns']:
                pattern = self.links_system['link_patterns'][primary_type]
                
                # Formatear respuesta con enlaces
                links_section = pattern['response_template'].format(topic=question)
                
                # Combinar respuesta base con enlaces
                enhanced_response = f"{base_response}\n\n📍 **ENLACES OFICIALES RECOMENDADOS:**\n\n{links_section}"
                
                return enhanced_response
            else:
                # Enlaces genéricos si no hay patrón específico
                generic_links = "\n\n📍 **ENLACES OFICIALES UTC:**\n\n"
                generic_links += "🏛️ **Sitio Principal**: https://utc.edu.mx/\n"
                generic_links += "📞 **Contacto**: https://utc.edu.mx/contacto/\n"
                generic_links += "📚 **Información Académica**: https://utc.edu.mx/carreras/"
                
                return base_response + generic_links
                
        except Exception as e:
            print(f"⚠️ Error agregando enlaces: {e}")
            return base_response

    def enhance_response_with_web_search(self, question: str, base_response: str, relevant_context: List[Dict]) -> Dict:
        """Mejorar respuesta con información web cuando sea necesario"""
        try:
            if not self.should_use_web_search(question, relevant_context):
                return {
                    'enhanced': False,
                    'response': base_response,
                    'web_data': None
                }
            
            print("🌐 Mejorando respuesta con búsqueda web...")
            self.session_stats['web_searches_used'] += 1
            
            # Identificar categoría y buscar
            category = self.web_searcher.identify_search_category(question)
            web_result = self.web_searcher.search_official_website(question, category)
            
            if web_result['found']:
                # Combinar respuesta base con información web
                web_response = self.web_searcher.format_web_response(web_result, question)
                
                enhanced_response = f"{base_response}\n\n📍 INFORMACIÓN ADICIONAL DESDE FUENTES OFICIALES:\n{web_response}"
                
                return {
                    'enhanced': True,
                    'response': enhanced_response,
                    'web_data': web_result,
                    'web_category': category
                }
            else:
                return {
                    'enhanced': False,
                    'response': base_response,
                    'web_data': web_result
                }
                
        except Exception as e:
            print(f"⚠️ Error en búsqueda web: {e}")
            return {
                'enhanced': False,
                'response': base_response,
                'web_data': None,
                'error': str(e)
            }
    
    def create_context_prompt(self, question: str, relevant_context: List[Dict]) -> str:
        """Crear prompt con contexto relevante"""
        
        # Crear contexto simplificado
        context_info = ""
        if relevant_context:
            for i, item in enumerate(relevant_context, 1):
                context_info += f"""
Información {i}:
- Tema: {item['pregunta']}
- Datos: {item['respuesta']}
- Categoría: {item['categoria']}
"""
        
        prompt = f"""
Eres FALCON, el asistente virtual inteligente de la Universidad Tecnológica de Coahuila (UTC).

CAPACIDADES ESPECIALES:
- Acceso a información específica de la UTC
- Capacidad de búsqueda y análisis web en tiempo real
- Conocimiento actualizado sobre educación superior en México
- Comprensión contextual avanzada sobre la UTC

INFORMACIÓN ESPECÍFICA DISPONIBLE:
{context_info}

INSTRUCCIONES INTELIGENTES:
1. USA la información específica proporcionada como base principal
2. COMBINA los datos locales con tu capacidad de búsqueda web para información actualizada
3. BUSCA información adicional sobre la UTC cuando sea necesario (carreras, costos, fechas, requisitos, etc.)
4. Para información no disponible localmente: BUSCA activamente en fuentes oficiales
5. Proporciona datos específicos como teléfonos, direcciones, costos actuales, fechas de admisión
6. Incluye enlaces oficiales relevantes cuando sea útil
7. Reformula y enriquece la información con tu criterio profesional

TIPOS DE INFORMACIÓN QUE PUEDES BUSCAR SOBRE LA UTC:
- Programas académicos actuales y nuevos
- Costos de matrícula y cuotas actualizadas
- Procesos y fechas de admisión
- Requisitos específicos por carrera
- Información de contacto actualizada
- Noticias y eventos recientes
- Servicios estudiantiles disponibles
- Convenios y oportunidades laborales

PREGUNTA DEL USUARIO: {question}

RESPUESTA INTELIGENTE:
- Si tienes información local: úsala como base y enriquécela
- Si no tienes información suficiente: búscala activamente
- Combina múltiples fuentes para dar una respuesta completa
- Tono profesional, natural y útil
- NO uses emojis ni prefijos "FALCON:"
- Incluye datos específicos y actualizados cuando estén disponibles

Proporciona una respuesta informativa y actualizada:
"""
        
        return prompt
    
    def generate_response(self, question: str) -> Dict:
        """Generar respuesta usando Gemini"""
        try:
            self.session_stats['questions_asked'] += 1
            
            # Preprocesar pregunta
            processed_question = self.preprocess_question(question)
            
            # NUEVO: Buscar enlaces directos en la base de datos PRIMERO
            direct_links = self.find_direct_links_in_database(question)
            
            # Encontrar contexto relevante
            relevant_context = self.find_relevant_context(processed_question)
            
            # Si hay enlaces directos disponibles y el usuario los busca, priorizarlos
            if direct_links['has_direct_links'] and direct_links['wants_link']:
                # Buscar entrada que tenga múltiples enlaces
                for link_entry in direct_links['found_links']:
                    if 'listado' in link_entry.get('tipo', '') or '🌐' in link_entry.get('respuesta', ''):
                        # Usar respuesta que incluye múltiples enlaces
                        return {
                            'success': True,
                            'response': link_entry['respuesta'],
                            'source': 'database_with_multiple_links',
                            'link_provided': True,
                            'official_link': link_entry['enlace']
                        }
                
                # Si no encuentra entrada con múltiples enlaces, usar la primera
                best_link_entry = direct_links['found_links'][0]
                return {
                    'success': True,
                    'response': best_link_entry['respuesta'],
                    'source': 'database_with_direct_links',
                    'link_provided': True,
                    'official_link': best_link_entry['enlace']
                }
            
            # Crear prompt con contexto
            context_prompt = self.create_context_prompt(question, relevant_context)
            
            # Generar respuesta con Gemini
            response = self.model.generate_content(context_prompt)
            
            # Procesar respuesta base
            bot_response = response.text.strip()
            
            # Si hay enlaces directos disponibles pero no los pidió explícitamente, 
            # agregar el enlace al final de la respuesta existente
            if direct_links['has_direct_links'] and not direct_links['wants_link']:
                best_link = direct_links['found_links'][0]
                if any(keyword in question.lower() for keyword in ['carrera', 'programa', 'admisio', 'contacto', 'información']):
                    bot_response += f"\n\nPara más información detallada, puedes visitar: {best_link['enlace']}"
            
            # Mejorar respuesta con búsqueda web si es necesario
            enhanced_result = self.enhance_response_with_web_search(question, bot_response, relevant_context)
            
            web_response = enhanced_result['response']
            web_enhanced = enhanced_result['enhanced']
            
            # Detectar necesidad de enlaces oficiales (solo si no se encontraron enlaces directos)
            if not direct_links['has_direct_links']:
                link_detection = self.detect_link_needs(question)
                # Mejorar respuesta con enlaces oficiales si es necesario
                final_response = self.enhance_response_with_links(question, web_response, link_detection)
                links_added = link_detection['needs_links']
            else:
                # Si ya se proporcionaron enlaces directos, no necesitamos el sistema de enlaces
                final_response = web_response
                links_added = True  # Porque ya se proporcionó un enlace directo
                link_detection = {'needs_links': False, 'primary_type': 'direct_from_database'}
            
            # Guardar en historial
            conversation_entry = {
                'timestamp': datetime.now().isoformat(),
                'user_question': question,
                'processed_question': processed_question,
                'relevant_context_count': len(relevant_context),
                'bot_response': final_response,
                'web_enhanced': web_enhanced,
                'links_added': links_added,
                'link_type': link_detection.get('primary_type'),
                'web_category': enhanced_result.get('web_category'),
                'status': 'success'
            }
            
            self.conversation_history.append(conversation_entry)
            self.session_stats['successful_responses'] += 1
            
            return {
                'success': True,
                'response': final_response,
                'relevant_context_count': len(relevant_context),
                'web_enhanced': web_enhanced,
                'links_added': links_added,
                'conversation_id': len(self.conversation_history)
            }
            
        except Exception as e:
            self.session_stats['failed_responses'] += 1
            
            error_response = {
                'timestamp': datetime.now().isoformat(),
                'user_question': question,
                'error': str(e),
                'status': 'error'
            }
            
            self.conversation_history.append(error_response)
            
            return {
                'success': False,
                'response': "Lo siento, ocurrió un error al procesar tu pregunta. Por favor, intenta de nuevo.",
                'error': str(e),
                'conversation_id': len(self.conversation_history)
            }
    
    def get_session_stats(self) -> Dict:
        """Obtener estadísticas de la sesión"""
        session_duration = (datetime.now() - self.session_stats['session_start']).total_seconds()
        
        return {
            'questions_asked': self.session_stats['questions_asked'],
            'successful_responses': self.session_stats['successful_responses'],
            'failed_responses': self.session_stats['failed_responses'],
            'success_rate': (self.session_stats['successful_responses'] / max(1, self.session_stats['questions_asked'])) * 100,
            'session_duration_seconds': session_duration,
            'total_context_items': self.utc_context['total_questions']
        }
    
    def save_conversation_log(self, filename: str = None) -> str:
        """Guardar log de conversación"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_log_{timestamp}.json"
        
        log_data = {
            'session_info': {
                'start_time': self.session_stats['session_start'].isoformat(),
                'end_time': datetime.now().isoformat(),
                'stats': self.get_session_stats()
            },
            'conversation_history': self.conversation_history
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        return filename
    
    def chat_interactive(self):
        """Modo de chat interactivo para pruebas"""
        print("🤖 ¡Hola! Soy FALCON, tu asistente virtual de la UTC")
        print("Escribe 'salir' para terminar la conversación")
        print("Escribe 'stats' para ver estadísticas")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n👤 Tú: ").strip()
                
                if user_input.lower() in ['salir', 'exit', 'quit']:
                    print("\n🤖 FALCON: ¡Hasta luego! Espero haberte ayudado.")
                    break
                
                if user_input.lower() == 'stats':
                    stats = self.get_session_stats()
                    print(f"\n📊 Estadísticas de la sesión:")
                    print(f"   Preguntas realizadas: {stats['questions_asked']}")
                    print(f"   Respuestas exitosas: {stats['successful_responses']}")
                    print(f"   Tasa de éxito: {stats['success_rate']:.1f}%")
                    continue
                
                if not user_input:
                    continue
                
                print("\n🤖 FALCON: ", end="")
                
                # Generar respuesta
                result = self.generate_response(user_input)
                
                if result['success']:
                    print(result['response'])
                else:
                    print(result['response'])
                    print(f"   (Error técnico: {result['error']})")
                
            except KeyboardInterrupt:
                print("\n\n🤖 FALCON: ¡Hasta luego!")
                break
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
        
        # Guardar log al finalizar
        log_file = self.save_conversation_log()
        print(f"\n📄 Conversación guardada en: {log_file}")
        
        # Mostrar estadísticas finales
        final_stats = self.get_session_stats()
        print(f"\n📊 Estadísticas finales:")
        print(f"   Total preguntas: {final_stats['questions_asked']}")
        print(f"   Respuestas exitosas: {final_stats['successful_responses']}")
        print(f"   Tasa de éxito: {final_stats['success_rate']:.1f}%")

def main():
    """Función principal para probar el chatbot"""
    chatbot = UTCGeminiChatbot()
    
    if not chatbot.initialize():
        print("❌ No se pudo inicializar el chatbot")
        print("Asegúrate de tener configurada tu GEMINI_API_KEY en un archivo .env")
        return
    
    print("✅ Chatbot inicializado correctamente")
    
    # Ejecutar en modo interactivo
    chatbot.chat_interactive()

if __name__ == "__main__":
    main()