import sqlite3
import os

# Conectar a la base de datos
db_path = 'db.sqlite3'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=== TABLAS EN LA BASE DE DATOS ===")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(f"- {table[0]}")
    
    print("\n=== ESTRUCTURA DE LA TABLA Database (cross_asistent_database) ===")
    try:
        cursor.execute("PRAGMA table_info(cross_asistent_database);")
        columns = cursor.fetchall()
        for col in columns:
            print(f"- {col[1]} ({col[2]})")
    except:
        print("Tabla cross_asistent_database no encontrada")
    
    print("\n=== CONTEO DE REGISTROS EN TABLAS PRINCIPALES ===")
    important_tables = [
        'cross_asistent_database',
        'cross_asistent_preguntas',
        'cross_asistent_categorias'
    ]
    
    for table in important_tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"- {table}: {count} registros")
        except Exception as e:
            print(f"- {table}: Error - {e}")
    
    print("\n=== MUESTRA DE DATOS DE LA TABLA Database ===")
    try:
        cursor.execute("SELECT id, titulo, informacion, categoria_id FROM cross_asistent_database LIMIT 5;")
        records = cursor.fetchall()
        for record in records:
            print(f"ID: {record[0]} | Título: {record[1][:50]}... | Categoría ID: {record[3]}")
    except Exception as e:
        print(f"Error al obtener datos: {e}")
    
    print("\n=== MUESTRA DE CATEGORÍAS ===")
    try:
        cursor.execute("SELECT id, categoria FROM cross_asistent_categorias;")
        categories = cursor.fetchall()
        for cat in categories:
            print(f"ID: {cat[0]} | Categoría: {cat[1]}")
    except Exception as e:
        print(f"Error al obtener categorías: {e}")
    
    conn.close()
else:
    print("Base de datos no encontrada en la ruta especificada")