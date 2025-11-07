"""
Entrenador Gemini para la Universidad Tecnológica de Coahuila
Prepara y optimiza los datos para el chatbot inteligente
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple
import google.generativeai as genai
from gemini_config import GeminiConfig

class GeminiTrainer:
    """
    Entrenador especializado para Gemini con datos de la UTC
    """
    
    def __init__(self):
        self.config = GeminiConfig()
        self.model = None
        self.utc_context = None
        self.training_examples = []
        
    def initialize(self):
        """Inicializar el entrenador"""
        try:
            print("🚀 Inicializando Entrenador Gemini para UTC...")
            
            # Inicializar modelo
            self.model = self.config.initialize_gemini()
            print("✅ Modelo Gemini inicializado")
            
            # Cargar contexto UTC
            self.utc_context = self.config.load_utc_context()
            print(f"✅ Contexto UTC cargado: {self.utc_context['total_questions']} preguntas")
            
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando entrenador: {e}")
            return False
    
    def prepare_training_examples(self):
        """Preparar ejemplos de entrenamiento optimizados"""
        print("📚 Preparando ejemplos de entrenamiento...")
        
        knowledge_base = self.utc_context['knowledge_base']
        
        # Crear ejemplos de conversación
        self.training_examples = []
        
        for item in knowledge_base:
            pregunta = item['pregunta']
            respuesta = item['respuesta']
            categoria = item['categoria']
            
            # Crear variaciones de la pregunta
            example = {
                'input': pregunta,
                'output': respuesta,
                'categoria': categoria,
                'variations': self._generate_question_variations(pregunta)
            }
            
            self.training_examples.append(example)
        
        print(f"✅ {len(self.training_examples)} ejemplos preparados")
        return self.training_examples
    
    def _generate_question_variations(self, pregunta: str) -> List[str]:
        """Generar variaciones de preguntas para mejorar el matching"""
        variations = [pregunta]
        
        # Variaciones comunes
        if "Tecnico Superior Universitario" in pregunta:
            variations.append(pregunta.replace("Tecnico Superior Universitario", "TSU"))
            variations.append(pregunta.replace("Tecnico Superior Universitario(T.S.U.)", "TSU"))
        
        if "Licenciatura" in pregunta:
            variations.append(pregunta.replace("Licenciatura", "Lic"))
        
        # Agregar palabras clave
        keywords = self._extract_keywords(pregunta)
        for keyword in keywords:
            if len(keyword) > 3:
                variations.append(f"¿Qué sabes sobre {keyword}?")
                variations.append(f"Información de {keyword}")
                variations.append(f"Cuéntame sobre {keyword}")
        
        return list(set(variations))
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extraer palabras clave importantes del texto"""
        # Palabras comunes a ignorar
        stop_words = {'de', 'la', 'el', 'en', 'y', 'a', 'que', 'es', 'se', 'no', 'te', 'lo', 
                     'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'una', 'del', 'las'}
        
        words = text.lower().split()
        keywords = [word.strip('.,():-') for word in words 
                   if len(word) > 3 and word.lower() not in stop_words]
        
        return keywords[:5]  # Limitar a 5 keywords
    
    def create_knowledge_embeddings(self):
        """Crear embeddings del conocimiento para búsqueda semántica"""
        print("🧠 Creando embeddings de conocimiento...")
        
        embeddings_data = []
        
        for example in self.training_examples:
            # Crear embedding para la pregunta principal
            embedding_item = {
                'text': example['input'],
                'response': example['output'],
                'categoria': example['categoria'],
                'type': 'question'
            }
            embeddings_data.append(embedding_item)
            
            # Crear embeddings para variaciones
            for variation in example['variations']:
                embedding_item = {
                    'text': variation,
                    'response': example['output'],
                    'categoria': example['categoria'],
                    'type': 'variation'
                }
                embeddings_data.append(embedding_item)
        
        # Guardar embeddings
        embeddings_file = 'utc_knowledge_embeddings.json'
        with open(embeddings_file, 'w', encoding='utf-8') as f:
            json.dump(embeddings_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {len(embeddings_data)} embeddings creados en {embeddings_file}")
        return embeddings_data
    
    def test_model_responses(self, test_questions: List[str] = None):
        """Probar respuestas del modelo con preguntas de prueba"""
        print("🧪 Probando respuestas del modelo...")
        
        if test_questions is None:
            test_questions = [
                "¿Qué carreras ofrece la UTC?",
                "¿Cuándo son los exámenes de admisión?",
                "¿Dónde está la biblioteca?",
                "¿Quién es el rector?",
                "¿Cómo puedo obtener una beca?"
            ]
        
        system_prompt = self.config.get_system_prompt(self.utc_context)
        
        test_results = []
        
        for question in test_questions:
            try:
                # Crear contexto completo
                full_prompt = f"{system_prompt}\n\nPregunta del usuario: {question}"
                
                # Generar respuesta
                response = self.model.generate_content(full_prompt)
                
                result = {
                    'question': question,
                    'response': response.text,
                    'status': 'success'
                }
                
                print(f"✅ P: {question}")
                print(f"   R: {response.text[:100]}...")
                print()
                
            except Exception as e:
                result = {
                    'question': question,
                    'response': f"Error: {e}",
                    'status': 'error'
                }
                print(f"❌ Error con pregunta: {question} - {e}")
            
            test_results.append(result)
        
        # Guardar resultados de prueba
        test_file = f'test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_results, f, ensure_ascii=False, indent=2)
        
        print(f"📊 Resultados guardados en {test_file}")
        return test_results
    
    def generate_enhanced_prompt(self):
        """Generar prompt mejorado con toda la información de la UTC"""
        print("📝 Generando prompt mejorado...")
        
        # Organizar información por categorías
        categorized_info = {}
        for item in self.utc_context['knowledge_base']:
            categoria = item['categoria']
            if categoria not in categorized_info:
                categorized_info[categoria] = []
            
            categorized_info[categoria].append({
                'q': item['pregunta'],
                'a': item['respuesta']
            })
        
        # Crear prompt estructurado
        enhanced_prompt = f"""
Eres FALCON, el asistente virtual oficial de la Universidad Tecnológica de Coahuila (UTC).

INFORMACIÓN INSTITUCIONAL COMPLETA:

"""
        
        for categoria, items in categorized_info.items():
            enhanced_prompt += f"\n=== {categoria.upper()} ===\n"
            for item in items:
                enhanced_prompt += f"P: {item['q']}\n"
                enhanced_prompt += f"R: {item['a']}\n\n"
        
        enhanced_prompt += """
INSTRUCCIONES DE RESPUESTA:
1. Responde SIEMPRE en español
2. Usa la información exacta proporcionada arriba
3. Si la pregunta no está en tu base de conocimientos, di que no tienes esa información específica
4. Sé amigable y profesional
5. Proporciona detalles relevantes como fechas, ubicaciones, y procedimientos
6. Si mencionas eventos, incluye fechas y horarios cuando estén disponibles

ESTILO:
- Saluda como "¡Hola! Soy FALCON, tu asistente virtual de la UTC"
- Usa emojis ocasionalmente para ser más amigable
- Termina preguntando si necesita más información

¿En qué puedo ayudarte hoy sobre la Universidad Tecnológica de Coahuila?
"""
        
        # Guardar prompt mejorado
        prompt_file = 'utc_enhanced_prompt.txt'
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_prompt)
        
        print(f"✅ Prompt mejorado guardado en {prompt_file}")
        return enhanced_prompt
    
    def run_full_training(self):
        """Ejecutar proceso completo de entrenamiento"""
        print("🎓 Iniciando entrenamiento completo de Gemini para UTC...")
        
        # Paso 1: Inicializar
        if not self.initialize():
            return False
        
        # Paso 2: Preparar ejemplos
        self.prepare_training_examples()
        
        # Paso 3: Crear embeddings
        self.create_knowledge_embeddings()
        
        # Paso 4: Generar prompt mejorado
        self.generate_enhanced_prompt()
        
        # Paso 5: Probar modelo
        self.test_model_responses()
        
        print("🎉 ¡Entrenamiento completado exitosamente!")
        print("\nArchivos generados:")
        print("- utc_knowledge_embeddings.json")
        print("- utc_enhanced_prompt.txt")
        print("- test_results_[timestamp].json")
        
        return True

def main():
    """Función principal para ejecutar el entrenamiento"""
    trainer = GeminiTrainer()
    success = trainer.run_full_training()
    
    if success:
        print("\n✅ El chatbot está listo para usar!")
        print("\nPasos siguientes:")
        print("1. Configura tu GEMINI_API_KEY en un archivo .env")
        print("2. Integra el chatbot con Django")
        print("3. ¡Prueba el chatbot en tu aplicación!")
    else:
        print("\n❌ Hubo errores en el entrenamiento")
        print("Revisa la configuración de la API key")

if __name__ == "__main__":
    main()