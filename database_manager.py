#!/usr/bin/env python3
"""
Sistema de Gestión Dinámica de Base de Datos UTC-FALCON
Permite agregar, modificar y gestionar información de manera flexible
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class UTCDatabaseManager:
    """Gestor avanzado de la base de datos UTC"""
    
    def __init__(self):
        self.base_dir = os.path.dirname(__file__)
        self.data_dir = os.path.join(self.base_dir, 'exported_data')
        self.current_file = os.path.join(self.data_dir, 'utc_training_data_20251105_192821.json')
        self.backup_dir = os.path.join(self.data_dir, 'backups')
        
        # Crear directorios si no existen
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def load_current_data(self) -> List[Dict]:
        """Cargar datos actuales"""
        try:
            with open(self.current_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Archivo de datos no encontrado")
            return []
    
    def save_data(self, data: List[Dict], create_backup: bool = True) -> bool:
        """Guardar datos con respaldo automático"""
        try:
            # Crear backup si se solicita
            if create_backup and os.path.exists(self.current_file):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = os.path.join(self.backup_dir, f'backup_{timestamp}.json')
                with open(self.current_file, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
                with open(backup_file, 'w', encoding='utf-8') as f:
                    json.dump(backup_data, f, ensure_ascii=False, indent=2)
                print(f"💾 Backup creado: {backup_file}")
            
            # Guardar datos actualizados
            with open(self.current_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Datos guardados: {len(data)} entradas")
            return True
            
        except Exception as e:
            print(f"❌ Error guardando datos: {e}")
            return False
    
    def add_single_entry(self, pregunta: str, respuesta: str, categoria: str = "general", palabras_clave: List[str] = None) -> bool:
        """Agregar una sola entrada"""
        data = self.load_current_data()
        
        new_entry = {
            "pregunta": pregunta,
            "respuesta": respuesta,
            "categoria": categoria,
            "palabras_clave": palabras_clave or [],
            "fecha_agregado": datetime.now().isoformat(),
            "version": "manual_v1.0"
        }
        
        data.append(new_entry)
        return self.save_data(data)
    
    def add_multiple_entries(self, entries: List[Dict]) -> bool:
        """Agregar múltiples entradas"""
        data = self.load_current_data()
        
        for entry in entries:
            entry["fecha_agregado"] = datetime.now().isoformat()
            entry["version"] = "batch_v1.0"
        
        data.extend(entries)
        return self.save_data(data)
    
    def find_entries(self, search_term: str) -> List[Dict]:
        """Buscar entradas por término"""
        data = self.load_current_data()
        found = []
        
        search_term = search_term.lower()
        
        for i, entry in enumerate(data):
            if (search_term in entry.get('pregunta', '').lower() or 
                search_term in entry.get('respuesta', '').lower() or
                search_term in ' '.join(entry.get('palabras_clave', [])).lower()):
                entry['index'] = i
                found.append(entry)
        
        return found
    
    def update_entry(self, index: int, updates: Dict) -> bool:
        """Actualizar una entrada específica"""
        data = self.load_current_data()
        
        if 0 <= index < len(data):
            data[index].update(updates)
            data[index]["fecha_modificado"] = datetime.now().isoformat()
            return self.save_data(data)
        else:
            print(f"❌ Índice {index} fuera de rango")
            return False
    
    def delete_entry(self, index: int) -> bool:
        """Eliminar una entrada"""
        data = self.load_current_data()
        
        if 0 <= index < len(data):
            deleted = data.pop(index)
            print(f"🗑️ Eliminado: {deleted.get('pregunta', 'Sin título')}")
            return self.save_data(data)
        else:
            print(f"❌ Índice {index} fuera de rango")
            return False
    
    def get_statistics(self) -> Dict:
        """Obtener estadísticas de la base de datos"""
        data = self.load_current_data()
        
        stats = {
            "total_entradas": len(data),
            "categorias": {},
            "palabras_clave_frecuentes": {},
            "fechas_recientes": []
        }
        
        for entry in data:
            # Categorías
            cat = entry.get('categoria', 'sin_categoria')
            stats["categorias"][cat] = stats["categorias"].get(cat, 0) + 1
            
            # Palabras clave
            for palabra in entry.get('palabras_clave', []):
                stats["palabras_clave_frecuentes"][palabra] = stats["palabras_clave_frecuentes"].get(palabra, 0) + 1
            
            # Fechas
            if 'fecha_agregado' in entry:
                stats["fechas_recientes"].append(entry['fecha_agregado'])
        
        return stats
    
    def interactive_menu(self):
        """Menú interactivo para gestionar la base de datos"""
        while True:
            print("\n" + "="*50)
            print("🎯 GESTOR DE BASE DE DATOS UTC-FALCON")
            print("="*50)
            print("1. 📊 Ver estadísticas")
            print("2. 🔍 Buscar entradas")
            print("3. ➕ Agregar entrada individual")
            print("4. 📝 Agregar múltiples entradas")
            print("5. ✏️ Editar entrada")
            print("6. 🗑️ Eliminar entrada")
            print("7. 📋 Listar todas las entradas")
            print("8. 🚪 Salir")
            print("-"*50)
            
            choice = input("Selecciona una opción (1-8): ").strip()
            
            if choice == "1":
                self.show_statistics()
            elif choice == "2":
                self.search_interactive()
            elif choice == "3":
                self.add_single_interactive()
            elif choice == "4":
                self.add_multiple_interactive()
            elif choice == "5":
                self.edit_interactive()
            elif choice == "6":
                self.delete_interactive()
            elif choice == "7":
                self.list_all_entries()
            elif choice == "8":
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción no válida")
    
    def show_statistics(self):
        """Mostrar estadísticas"""
        stats = self.get_statistics()
        print(f"\n📊 ESTADÍSTICAS DE LA BASE DE DATOS")
        print(f"Total de entradas: {stats['total_entradas']}")
        print(f"\n📂 Categorías:")
        for cat, count in stats['categorias'].items():
            print(f"  - {cat}: {count}")
        print(f"\n🏷️ Palabras clave más frecuentes:")
        sorted_keywords = sorted(stats['palabras_clave_frecuentes'].items(), 
                                key=lambda x: x[1], reverse=True)
        for keyword, count in sorted_keywords[:10]:
            print(f"  - {keyword}: {count}")
    
    def search_interactive(self):
        """Búsqueda interactiva"""
        search_term = input("\n🔍 Ingresa término de búsqueda: ").strip()
        if search_term:
            results = self.find_entries(search_term)
            print(f"\n📋 Encontradas {len(results)} entradas:")
            for result in results[:5]:  # Mostrar solo las primeras 5
                print(f"  [{result['index']}] {result['pregunta'][:80]}...")
    
    def add_single_interactive(self):
        """Agregar entrada individual de forma interactiva"""
        print("\n➕ AGREGAR NUEVA ENTRADA")
        pregunta = input("Pregunta: ").strip()
        respuesta = input("Respuesta: ").strip()
        categoria = input("Categoría (opcional): ").strip() or "general"
        palabras_input = input("Palabras clave (separadas por comas): ").strip()
        palabras_clave = [p.strip() for p in palabras_input.split(",")] if palabras_input else []
        
        if pregunta and respuesta:
            if self.add_single_entry(pregunta, respuesta, categoria, palabras_clave):
                print("✅ Entrada agregada exitosamente")
            else:
                print("❌ Error al agregar entrada")
        else:
            print("❌ Pregunta y respuesta son obligatorias")

# Scripts predefinidos para agregar información específica
def add_transport_complete_info():
    """Agregar información completa sobre transporte"""
    manager = UTCDatabaseManager()
    
    transport_entries = [
        {
            "pregunta": "¿La UTC ofrece servicio de transporte a los estudiantes?",
            "respuesta": "Actualmente la UTC no cuenta con un servicio de transporte propio para estudiantes. Sin embargo, la universidad está bien conectada con el transporte público de la región. Para información específica sobre rutas y opciones de movilidad, te recomiendo contactar al departamento de servicios estudiantiles.",
            "categoria": "servicios",
            "palabras_clave": ["transporte", "movilidad", "servicios estudiantiles", "transporte público", "estudiantes"]
        },
        {
            "pregunta": "¿Cómo puedo llegar a la UTC en transporte público?",
            "respuesta": "La UTC está ubicada en una zona accesible por transporte público. Para conocer las rutas específicas, horarios y paradas más cercanas, es recomendable consultar con el departamento de servicios estudiantiles, ya que ellos tienen la información más actualizada sobre las mejores opciones de transporte para llegar al campus.",
            "categoria": "ubicacion",
            "palabras_clave": ["transporte público", "rutas", "horarios", "ubicación", "campus", "como llegar"]
        },
        {
            "pregunta": "¿Hay descuentos de transporte para estudiantes UTC?",
            "respuesta": "Para información sobre posibles descuentos en transporte público o convenios especiales para estudiantes de la UTC, te sugiero consultar directamente en el departamento de servicios estudiantiles. Ellos pueden informarte sobre acuerdos vigentes y beneficios disponibles para la comunidad estudiantil.",
            "categoria": "servicios",
            "palabras_clave": ["descuentos", "convenios", "servicios estudiantiles", "beneficios", "estudiantes"]
        },
        {
            "pregunta": "¿Dónde está ubicada exactamente la UTC?",
            "respuesta": "La Universidad Tecnológica de Coahuila (UTC) está ubicada en el estado de Coahuila, México. Para obtener la dirección exacta, horarios de atención y cómo llegar, te recomiendo consultar el sitio web oficial de la universidad o contactar directamente con la administración.",
            "categoria": "ubicacion", 
            "palabras_clave": ["ubicación", "dirección", "Coahuila", "México", "campus"]
        }
    ]
    
    if manager.add_multiple_entries(transport_entries):
        print(f"✅ Se agregaron {len(transport_entries)} entradas sobre transporte y ubicación")
        stats = manager.get_statistics()
        print(f"📊 Total de entradas en la base de datos: {stats['total_entradas']}")
    else:
        print("❌ Error al agregar las entradas")

if __name__ == "__main__":
    print("🚀 Gestor de Base de Datos UTC-FALCON")
    print("1. Agregar información completa de transporte")
    print("2. Abrir menú interactivo")
    print("3. Solo mostrar estadísticas")
    
    option = input("Selecciona una opción (1-3): ").strip()
    
    if option == "1":
        add_transport_complete_info()
    elif option == "2":
        manager = UTCDatabaseManager()
        manager.interactive_menu()
    elif option == "3":
        manager = UTCDatabaseManager()
        manager.show_statistics()
    else:
        print("❌ Opción no válida")