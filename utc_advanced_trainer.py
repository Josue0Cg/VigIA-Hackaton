"""
Sistema de Entrenamiento Avanzado para el Chatbot UTC
Mejora la calidad de respuestas y el contexto específico
"""

import json
import os
from datetime import datetime
from typing import Dict, List

class UTCChatbotTrainer:
    """Sistema de entrenamiento avanzado para mejorar el chatbot"""
    
    def __init__(self):
        self.base_data_file = 'exported_data/utc_training_data_20251105_192821.json'
        self.enhanced_data_file = 'exported_data/utc_enhanced_training_data.json'
        self.conversation_logs_file = 'exported_data/conversation_logs.json'
        
    def load_base_data(self) -> List[Dict]:
        """Cargar datos base existentes"""
        try:
            with open(self.base_data_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"❌ Archivo base no encontrado: {self.base_data_file}")
            return []
    
    def enhance_training_data(self):
        """Mejorar y expandir los datos de entrenamiento"""
        base_data = self.load_base_data()
        enhanced_data = []
        
        # Agregar datos mejorados con variaciones de preguntas
        question_variations = {
            "rector": [
                "¿Quién es el rector?",
                "¿Cuál es el nombre del rector?",
                "¿Quién dirige la universidad?",
                "¿Quién es el director de la UTC?",
                "Dime el nombre del rector",
                "¿Cómo se llama el rector actual?",
                "Información del rector",
                "Rector de la UTC"
            ],
            "carreras": [
                "¿Qué carreras ofrece la UTC?",
                "¿Cuáles son los programas académicos?",
                "¿Qué puedo estudiar en la UTC?",
                "Lista de carreras disponibles",
                "Programas de estudio",
                "¿Qué ingenierías hay?",
                "Licenciaturas disponibles",
                "Opciones académicas"
            ],
            "ubicacion": [
                "¿Dónde está la UTC?",
                "¿Cuál es la dirección?",
                "¿Cómo llego a la universidad?",
                "Ubicación de la UTC",
                "¿En qué ciudad está?",
                "Dirección completa",
                "¿Dónde se encuentra?"
            ],
            "costos": [
                "¿Cuánto cuesta estudiar?",
                "¿Cuáles son las colegiaturas?",
                "Costos de inscripción",
                "¿Cuánto se paga?",
                "Precios de las carreras",
                "Gastos universitarios",
                "Cuotas escolares"
            ]
        }
        
        # Procesar datos existentes y agregar variaciones
        for item in base_data:
            enhanced_data.append(item)
            
            # Identificar tipo de pregunta y agregar variaciones
            pregunta_lower = item['pregunta'].lower()
            
            if any(word in pregunta_lower for word in ['rector', 'sergio', 'alberto', 'guadarrama']):
                for var in question_variations["rector"]:
                    if var.lower() != pregunta_lower:
                        enhanced_data.append({
                            "pregunta": var,
                            "respuesta": item['respuesta'],
                            "categoria": item['categoria'],
                            "enhanced": True,
                            "base_question": item['pregunta']
                        })
        
        # Agregar contexto mejorado para el rector
        rector_enhanced = {
            "pregunta": "Información completa del rector UTC",
            "respuesta": """Sergio Alberto Guadarrama Cortés es el rector de la Universidad Tecnológica de Coahuila. 
            
Datos personales:
- Fecha de nacimiento: 5 de agosto de 1965
- Lugar de nacimiento: Nueva Rosita, Coahuila
- Cargo: Rector de la UTC

Visión y logros principales:
- Modernización y transformación institucional
- Creación de Ciudad Universitaria con servicios integrales
- Renovación completa de cafeterías y espacios estudiantiles
- Actualización tecnológica con 125 nuevas computadoras
- Fortalecimiento de vínculos con la industria
- Posicionamiento de la UTC como referente de excelencia educativa

El rector Guadarrama Cortés lidera la universidad con una visión ambiciosa enfocada en la innovación educativa y la mejora continua de la infraestructura universitaria.""",
            "categoria": "Personal",
            "enhanced": True,
            "priority": "high"
        }
        enhanced_data.append(rector_enhanced)
        
        # Guardar datos mejorados
        with open(self.enhanced_data_file, 'w', encoding='utf-8') as file:
            json.dump(enhanced_data, file, ensure_ascii=False, indent=2)
        
        print(f"✅ Datos de entrenamiento mejorados")
        print(f"📊 Total de entradas: {len(enhanced_data)}")
        print(f"📁 Guardado en: {self.enhanced_data_file}")
        
        return enhanced_data
    
    def create_advanced_prompts(self):
        """Crear prompts avanzados para diferentes tipos de consultas"""
        prompts = {
            "rector_prompt": """
Para preguntas sobre el rector, siempre incluye:
- Nombre completo: Sergio Alberto Guadarrama Cortés
- Su visión de modernización
- Logros principales en infraestructura
- Enfoque en excelencia educativa
Mantén un tono respetuoso y profesional.
""",
            "carreras_prompt": """
Para preguntas sobre carreras:
- Lista las opciones disponibles (TSU e Ingenierías)
- Menciona duración (2 años TSU + 1.8 años Ingeniería)
- Incluye campos de trabajo
- Sugiere contactar para más detalles
""",
            "general_prompt": """
Para preguntas generales:
- Usa conocimiento específico de UTC cuando esté disponible
- Combina con conocimiento general si es apropiado
- Mantén respuestas naturales y conversacionales
- Sugiere recursos adicionales cuando sea necesario
"""
        }
        
        with open('exported_data/advanced_prompts.json', 'w', encoding='utf-8') as file:
            json.dump(prompts, file, ensure_ascii=False, indent=2)
        
        return prompts
    
    def log_conversation(self, question: str, response: str, context_used: int, user_feedback: str = None):
        """Registrar conversaciones para análisis posterior"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "response": response,
            "context_items_used": context_used,
            "user_feedback": user_feedback,
            "response_length": len(response),
            "contains_utc_info": any(word in response.lower() for word in ['utc', 'universidad', 'coahuila', 'sergio', 'rector'])
        }
        
        # Cargar logs existentes
        try:
            with open(self.conversation_logs_file, 'r', encoding='utf-8') as file:
                logs = json.load(file)
        except FileNotFoundError:
            logs = []
        
        logs.append(log_entry)
        
        # Guardar logs actualizados
        with open(self.conversation_logs_file, 'w', encoding='utf-8') as file:
            json.dump(logs, file, ensure_ascii=False, indent=2)
    
    def analyze_performance(self):
        """Analizar el rendimiento del chatbot"""
        try:
            with open(self.conversation_logs_file, 'r', encoding='utf-8') as file:
                logs = json.load(file)
        except FileNotFoundError:
            print("❌ No hay logs de conversación disponibles")
            return
        
        total_conversations = len(logs)
        utc_specific_responses = sum(1 for log in logs if log.get('contains_utc_info', False))
        avg_response_length = sum(log.get('response_length', 0) for log in logs) / total_conversations if total_conversations > 0 else 0
        
        print("📊 ANÁLISIS DE RENDIMIENTO DEL CHATBOT")
        print("=" * 50)
        print(f"Total de conversaciones: {total_conversations}")
        print(f"Respuestas con info UTC: {utc_specific_responses} ({utc_specific_responses/total_conversations*100:.1f}%)")
        print(f"Longitud promedio de respuesta: {avg_response_length:.0f} caracteres")
        
        # Preguntas más frecuentes
        questions = [log['question'].lower() for log in logs]
        question_words = {}
        for q in questions:
            for word in q.split():
                if len(word) > 3:
                    question_words[word] = question_words.get(word, 0) + 1
        
        top_words = sorted(question_words.items(), key=lambda x: x[1], reverse=True)[:10]
        print("\nPalabras más consultadas:")
        for word, count in top_words:
            print(f"  {word}: {count} veces")

def run_training_enhancement():
    """Ejecutar mejoras de entrenamiento"""
    print("🚀 INICIANDO ENTRENAMIENTO AVANZADO")
    print("=" * 50)
    
    trainer = UTCChatbotTrainer()
    
    # Mejorar datos de entrenamiento
    enhanced_data = trainer.enhance_training_data()
    
    # Crear prompts avanzados
    prompts = trainer.create_advanced_prompts()
    print("✅ Prompts avanzados creados")
    
    # Analizar rendimiento si hay logs
    trainer.analyze_performance()
    
    print("\n🎯 ENTRENAMIENTO COMPLETADO")
    print(f"📈 Base de datos expandida a {len(enhanced_data)} entradas")
    print("💡 Recomendaciones:")
    print("  1. Reinicia el servidor Django para aplicar cambios")
    print("  2. Prueba preguntas sobre el rector y carreras")
    print("  3. Observa mejoras en respuestas específicas")

if __name__ == "__main__":
    run_training_enhancement()