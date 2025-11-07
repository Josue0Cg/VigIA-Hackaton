"""
Sistema de Búsqueda Web Inteligente para el Chatbot UTC
Permite buscar información en tiempo real desde fuentes oficiales
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse
import time

class UTCWebSearcher:
    """Sistema de búsqueda web para información oficial de la UTC"""
    
    def __init__(self):
        self.official_sources = [
            "https://utc.edu.mx/",
            "https://www.utc.edu.mx/",
            "https://utcoahuila.edu.mx/",
        ]
        
        self.search_patterns = {
            'costos': [
                'costo', 'cuota', 'precio', 'inscripción', 'colegiatura', 
                'pago', 'arancel', 'tarifa'
            ],
            'ubicacion': [
                'dirección', 'ubicación', 'domicilio', 'donde', 'lugar',
                'campus', 'instalaciones'
            ],
            'contacto': [
                'teléfono', 'email', 'contacto', 'oficina', 'horario'
            ],
            'eventos': [
                'evento', 'ceremonia', 'graduación', 'fecha', 'calendario'
            ],
            'admisiones': [
                'admisión', 'ingreso', 'requisito', 'proceso', 'convocatoria'
            ]
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def identify_search_category(self, question: str) -> str:
        """Identificar qué tipo de información se está buscando"""
        question_lower = question.lower()
        
        for category, keywords in self.search_patterns.items():
            if any(keyword in question_lower for keyword in keywords):
                return category
        
        return 'general'
    
    def search_official_website(self, query: str, category: str = 'general') -> Dict:
        """Buscar información en el sitio web oficial de la UTC"""
        try:
            print(f"🌐 Buscando información web sobre: {query}")
            
            # Intentar diferentes URLs oficiales
            for base_url in self.official_sources:
                try:
                    response = requests.get(base_url, headers=self.headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Buscar información específica según la categoría
                        if category == 'costos':
                            info = self.extract_cost_info(soup, base_url)
                        elif category == 'ubicacion':
                            info = self.extract_location_info(soup, base_url)
                        elif category == 'contacto':
                            info = self.extract_contact_info(soup, base_url)
                        else:
                            info = self.extract_general_info(soup, base_url, query)
                        
                        if info['found']:
                            return info
                            
                except Exception as e:
                    print(f"⚠️ Error accediendo a {base_url}: {e}")
                    continue
            
            return {
                'found': False,
                'source': None,
                'data': None,
                'message': 'No se pudo acceder a las fuentes oficiales'
            }
            
        except Exception as e:
            print(f"❌ Error en búsqueda web: {e}")
            return {
                'found': False,
                'source': None,
                'data': None,
                'error': str(e)
            }
    
    def extract_cost_info(self, soup: BeautifulSoup, base_url: str) -> Dict:
        """Extraer información de costos y colegiaturas"""
        cost_info = {
            'found': False,
            'source': base_url,
            'data': {},
            'text': ""
        }
        
        # Buscar elementos que contengan información de costos
        cost_elements = soup.find_all(text=re.compile(r'costo|cuota|inscripción|colegiatura', re.I))
        
        if cost_elements:
            # Extraer contexto alrededor de los elementos encontrados
            for element in cost_elements[:3]:  # Limitar a 3 elementos
                parent = element.parent
                if parent:
                    cost_info['text'] += f"{parent.get_text().strip()} "
            
            cost_info['found'] = True
            cost_info['data']['type'] = 'costos'
            cost_info['data']['summary'] = cost_info['text'][:300] + "..."
        
        return cost_info
    
    def extract_location_info(self, soup: BeautifulSoup, base_url: str) -> Dict:
        """Extraer información de ubicación y direcciones"""
        location_info = {
            'found': False,
            'source': base_url,
            'data': {},
            'text': ""
        }
        
        # Buscar elementos con información de ubicación
        location_patterns = [
            r'dirección|ubicación|domicilio',
            r'campus|instalaciones',
            r'coahuila|torreón|laredo'
        ]
        
        for pattern in location_patterns:
            location_elements = soup.find_all(text=re.compile(pattern, re.I))
            
            if location_elements:
                for element in location_elements[:2]:
                    parent = element.parent
                    if parent:
                        location_info['text'] += f"{parent.get_text().strip()} "
                
                location_info['found'] = True
                location_info['data']['type'] = 'ubicacion'
                break
        
        return location_info
    
    def extract_contact_info(self, soup: BeautifulSoup, base_url: str) -> Dict:
        """Extraer información de contacto"""
        contact_info = {
            'found': False,
            'source': base_url,
            'data': {},
            'text': ""
        }
        
        # Buscar números de teléfono
        phone_pattern = r'\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})'
        phones = re.findall(phone_pattern, soup.get_text())
        
        # Buscar emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, soup.get_text())
        
        if phones or emails:
            contact_info['found'] = True
            contact_info['data']['phones'] = phones
            contact_info['data']['emails'] = emails
            contact_info['text'] = f"Teléfonos: {phones} | Emails: {emails}"
        
        return contact_info
    
    def extract_general_info(self, soup: BeautifulSoup, base_url: str, query: str) -> Dict:
        """Extraer información general relacionada con la consulta"""
        general_info = {
            'found': False,
            'source': base_url,
            'data': {},
            'text': ""
        }
        
        # Buscar elementos que contengan palabras clave de la consulta
        query_words = [word.lower() for word in query.split() if len(word) > 3]
        
        for word in query_words:
            elements = soup.find_all(text=re.compile(word, re.I))
            
            if elements:
                for element in elements[:2]:
                    parent = element.parent
                    if parent:
                        text = parent.get_text().strip()
                        if len(text) > 20:  # Filtrar textos muy cortos
                            general_info['text'] += f"{text[:200]} "
                
                if general_info['text']:
                    general_info['found'] = True
                    general_info['data']['query'] = query
                    break
        
        return general_info
    
    def format_web_response(self, web_result: Dict, question: str) -> str:
        """Formatear la respuesta con información web encontrada"""
        if not web_result['found']:
            return "No pude encontrar información específica en las fuentes oficiales en este momento. Te recomiendo visitar directamente el sitio web oficial de la UTC (utc.edu.mx) o contactar a la universidad para obtener la información más actualizada."
        
        response = f"Según la información disponible en el sitio web oficial de la UTC:\n\n"
        
        if web_result.get('text'):
            # Limpiar y formatear el texto extraído
            clean_text = re.sub(r'\s+', ' ', web_result['text']).strip()
            response += f"{clean_text}\n\n"
        
        response += f"📍 Fuente: {web_result['source']}\n"
        response += f"💡 Para información más detallada y actualizada, te recomiendo visitar el sitio web oficial de la UTC."
        
        return response

def test_web_search():
    """Función de prueba para el sistema de búsqueda web"""
    print("🧪 PROBANDO SISTEMA DE BÚSQUEDA WEB")
    print("=" * 50)
    
    searcher = UTCWebSearcher()
    
    test_queries = [
        ("¿Cuánto cuesta estudiar en la UTC?", "costos"),
        ("¿Dónde está ubicada la universidad?", "ubicacion"),
        ("¿Cuál es el teléfono de la UTC?", "contacto"),
        ("Información general sobre la UTC", "general")
    ]
    
    for query, expected_category in test_queries:
        print(f"\n🔍 Consulta: {query}")
        
        # Identificar categoría
        category = searcher.identify_search_category(query)
        print(f"📂 Categoría detectada: {category} (esperada: {expected_category})")
        
        # Buscar información
        result = searcher.search_official_website(query, category)
        
        if result['found']:
            print(f"✅ Información encontrada desde: {result['source']}")
            print(f"📝 Datos: {result.get('text', 'N/A')[:100]}...")
        else:
            print(f"❌ No se encontró información específica")
            print(f"💭 Mensaje: {result.get('message', 'N/A')}")

if __name__ == "__main__":
    test_web_search()