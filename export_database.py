import sqlite3
import json
import csv
import os
from datetime import datetime

def export_database():
    """Exporta la base de datos en múltiples formatos"""
    
    # Conectar a la base de datos
    db_path = 'db.sqlite3'
    if not os.path.exists(db_path):
        print("❌ Base de datos no encontrada")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Crear carpeta de exportación
    export_folder = 'exported_data'
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("🔄 Iniciando exportación de datos...")
    
    # 1. EXPORTAR DATOS COMPLETOS CON CATEGORÍAS
    print("\n📊 Exportando datos completos...")
    cursor.execute("""
        SELECT 
            d.id,
            d.titulo,
            d.informacion,
            c.categoria,
            d.frecuencia,
            d.fecha_modificacion,
            d.redirigir,
            d.evento_fecha_inicio,
            d.evento_fecha_fin,
            d.evento_lugar
        FROM cross_asistent_database d
        LEFT JOIN cross_asistent_categorias c ON d.categoria_id = c.id
        ORDER BY c.categoria, d.titulo;
    """)
    
    full_data = cursor.fetchall()
    columns = ['id', 'titulo', 'informacion', 'categoria', 'frecuencia', 'fecha_modificacion', 
               'redirigir', 'evento_fecha_inicio', 'evento_fecha_fin', 'evento_lugar']
    
    # Exportar a CSV
    csv_file = f'{export_folder}/utc_database_completa_{timestamp}.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(full_data)
    print(f"✅ CSV completo: {csv_file}")
    
    # Exportar a JSON
    json_data = []
    for row in full_data:
        json_data.append(dict(zip(columns, row)))
    
    json_file = f'{export_folder}/utc_database_completa_{timestamp}.json'
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=2, default=str)
    print(f"✅ JSON completo: {json_file}")
    
    # 2. EXPORTAR SOLO PREGUNTAS Y RESPUESTAS PARA ENTRENAMIENTO
    print("\n🤖 Exportando datos para entrenamiento de chatbot...")
    cursor.execute("""
        SELECT 
            d.titulo as pregunta,
            d.informacion as respuesta,
            c.categoria
        FROM cross_asistent_database d
        LEFT JOIN cross_asistent_categorias c ON d.categoria_id = c.id
        WHERE d.informacion IS NOT NULL AND d.informacion != ''
        ORDER BY c.categoria, d.titulo;
    """)
    
    training_data = cursor.fetchall()
    
    # CSV para entrenamiento
    training_csv = f'{export_folder}/utc_training_data_{timestamp}.csv'
    with open(training_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['pregunta', 'respuesta', 'categoria'])
        writer.writerows(training_data)
    print(f"✅ CSV entrenamiento: {training_csv}")
    
    # JSON para entrenamiento
    training_json_data = []
    for pregunta, respuesta, categoria in training_data:
        training_json_data.append({
            'pregunta': pregunta,
            'respuesta': respuesta,
            'categoria': categoria
        })
    
    training_json = f'{export_folder}/utc_training_data_{timestamp}.json'
    with open(training_json, 'w', encoding='utf-8') as file:
        json.dump(training_json_data, file, ensure_ascii=False, indent=2)
    print(f"✅ JSON entrenamiento: {training_json}")
    
    # 3. EXPORTAR POR CATEGORÍAS SEPARADAS
    print("\n📁 Exportando por categorías...")
    cursor.execute("SELECT id, categoria FROM cross_asistent_categorias;")
    categorias = cursor.fetchall()
    
    for cat_id, categoria in categorias:
        cursor.execute("""
            SELECT titulo, informacion
            FROM cross_asistent_database
            WHERE categoria_id = ? AND informacion IS NOT NULL AND informacion != ''
            ORDER BY titulo;
        """, (cat_id,))
        
        cat_data = cursor.fetchall()
        if cat_data:
            cat_file = f'{export_folder}/categoria_{categoria.lower().replace(" ", "_")}_{timestamp}.json'
            cat_json = []
            for titulo, info in cat_data:
                cat_json.append({
                    'pregunta': titulo,
                    'respuesta': info,
                    'categoria': categoria
                })
            
            with open(cat_file, 'w', encoding='utf-8') as file:
                json.dump(cat_json, file, ensure_ascii=False, indent=2)
            print(f"✅ {categoria}: {cat_file} ({len(cat_data)} registros)")
    
    # 4. EXPORTAR PREGUNTAS ESPECÍFICAS DE USUARIOS
    print("\n❓ Exportando preguntas de usuarios...")
    cursor.execute("SELECT pregunta, descripcion, fecha FROM cross_asistent_preguntas ORDER BY fecha;")
    user_questions = cursor.fetchall()
    
    if user_questions:
        user_q_file = f'{export_folder}/preguntas_usuarios_{timestamp}.json'
        user_q_data = []
        for pregunta, desc, fecha in user_questions:
            user_q_data.append({
                'pregunta': pregunta,
                'descripcion': desc,
                'fecha': fecha
            })
        
        with open(user_q_file, 'w', encoding='utf-8') as file:
            json.dump(user_q_data, file, ensure_ascii=False, indent=2, default=str)
        print(f"✅ Preguntas usuarios: {user_q_file} ({len(user_questions)} registros)")
    
    # 5. GENERAR REPORTE DE EXPORTACIÓN
    print("\n📋 Generando reporte...")
    report = {
        'fecha_exportacion': datetime.now().isoformat(),
        'total_registros': len(full_data),
        'registros_con_informacion': len(training_data),
        'registros_sin_informacion': len(full_data) - len(training_data),
        'categorias': [{'id': cat_id, 'nombre': categoria} for cat_id, categoria in categorias],
        'distribucion_por_categoria': {},
        'archivos_generados': []
    }
    
    # Calcular distribución por categoría
    for cat_id, categoria in categorias:
        cursor.execute("SELECT COUNT(*) FROM cross_asistent_database WHERE categoria_id = ?", (cat_id,))
        count = cursor.fetchone()[0]
        report['distribucion_por_categoria'][categoria] = count
    
    # Listar archivos generados
    for file in os.listdir(export_folder):
        if timestamp in file:
            report['archivos_generados'].append(file)
    
    report_file = f'{export_folder}/reporte_exportacion_{timestamp}.json'
    with open(report_file, 'w', encoding='utf-8') as file:
        json.dump(report, file, ensure_ascii=False, indent=2)
    
    print(f"✅ Reporte: {report_file}")
    
    # 6. GENERAR ARCHIVO TXT LEGIBLE
    txt_file = f'{export_folder}/utc_preguntas_respuestas_{timestamp}.txt'
    with open(txt_file, 'w', encoding='utf-8') as file:
        file.write("=" * 80 + "\n")
        file.write("PREGUNTAS Y RESPUESTAS - UNIVERSIDAD TECNOLÓGICA DE COAHUILA\n")
        file.write("=" * 80 + "\n\n")
        file.write(f"Fecha de exportación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        file.write(f"Total de registros: {len(training_data)}\n\n")
        
        current_category = None
        for pregunta, respuesta, categoria in training_data:
            if categoria != current_category:
                file.write("\n" + "=" * 60 + "\n")
                file.write(f"CATEGORÍA: {categoria.upper()}\n")
                file.write("=" * 60 + "\n\n")
                current_category = categoria
            
            file.write(f"PREGUNTA: {pregunta}\n")
            file.write(f"RESPUESTA: {respuesta}\n")
            file.write("-" * 40 + "\n\n")
    
    print(f"✅ Archivo legible: {txt_file}")
    
    conn.close()
    
    print(f"\n🎉 ¡Exportación completada!")
    print(f"📁 Todos los archivos están en: {os.path.abspath(export_folder)}")
    print(f"📊 Total de registros exportados: {len(training_data)} (con información)")
    print(f"📋 Total de archivos generados: {len(report['archivos_generados']) + 1}")

if __name__ == "__main__":
    export_database()