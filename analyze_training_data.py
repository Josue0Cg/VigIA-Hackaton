import sqlite3
import os

# Conectar a la base de datos
db_path = 'db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== ANÁLISIS DETALLADO DE LA BASE DE DATOS PARA ENTRENAMIENTO ===")

print("\n=== DISTRIBUCIÓN POR CATEGORÍAS ===")
cursor.execute("""
    SELECT c.categoria, COUNT(d.id) as cantidad 
    FROM cross_asistent_categorias c 
    LEFT JOIN cross_asistent_database d ON c.id = d.categoria_id 
    GROUP BY c.categoria 
    ORDER BY cantidad DESC;
""")
distribucion = cursor.fetchall()
for cat, count in distribucion:
    print(f"- {cat}: {count} registros")

print("\n=== EJEMPLOS DE PREGUNTAS Y RESPUESTAS POR CATEGORÍA ===")
for categoria, _ in distribucion:
    if categoria == "Preguntas":  # Evitamos la categoría vacía
        continue
    print(f"\n--- CATEGORÍA: {categoria.upper()} ---")
    cursor.execute("""
        SELECT d.titulo, d.informacion 
        FROM cross_asistent_database d 
        JOIN cross_asistent_categorias c ON d.categoria_id = c.id 
        WHERE c.categoria = ? 
        LIMIT 3;
    """, (categoria,))
    
    registros = cursor.fetchall()
    for i, (titulo, info) in enumerate(registros, 1):
        print(f"{i}. PREGUNTA: {titulo}")
        if info:
            info_preview = info[:200] + "..." if len(info) > 200 else info
            print(f"   RESPUESTA: {info_preview}")
        else:
            print("   RESPUESTA: (Sin información)")
        print()

print("\n=== TABLA DE PREGUNTAS ESPECÍFICAS ===")
cursor.execute("SELECT pregunta, descripcion, fecha FROM cross_asistent_preguntas;")
preguntas_especificas = cursor.fetchall()
for i, (pregunta, desc, fecha) in enumerate(preguntas_especificas, 1):
    print(f"{i}. {pregunta}")
    if desc:
        print(f"   Descripción: {desc}")
    print(f"   Fecha: {fecha}")
    print()

print("\n=== ESTADÍSTICAS GENERALES ===")
cursor.execute("SELECT COUNT(*) FROM cross_asistent_database WHERE informacion IS NOT NULL AND informacion != '';")
with_info = cursor.fetchone()[0]
print(f"- Registros con información: {with_info}")

cursor.execute("SELECT COUNT(*) FROM cross_asistent_database WHERE informacion IS NULL OR informacion = '';")
without_info = cursor.fetchone()[0]
print(f"- Registros sin información: {without_info}")

cursor.execute("SELECT AVG(LENGTH(informacion)) FROM cross_asistent_database WHERE informacion IS NOT NULL;")
avg_length = cursor.fetchone()[0]
print(f"- Longitud promedio de respuestas: {avg_length:.2f} caracteres")

conn.close()