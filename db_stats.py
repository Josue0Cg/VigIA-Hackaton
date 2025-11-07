#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cross_project.settings')
django.setup()

from cross_asistent.models import *
from django.contrib.auth.models import User

print("=" * 50)
print("         RESUMEN BASE DE DATOS FALCON")
print("=" * 50)

# Conteo general
print("\n📊 CONTEO DE REGISTROS:")
print(f"• Usuarios: {User.objects.count()}")
print(f"• Categorías: {Categorias.objects.count()}")
print(f"• Base de Datos (Contenido): {Database.objects.count()}")
print(f"• Banners: {Banners.objects.count()}")
print(f"• Artículos: {Articulos.objects.count()}")
print(f"• Puntos de Mapa: {Mapa.objects.count()}")
print(f"• Galería: {galeria.objects.count()}")
print(f"• Preguntas: {Preguntas.objects.count()}")
print(f"• Configuraciones: {Configuraciones.objects.count()}")
print(f"• Perfiles de Usuario: {UserProfile.objects.count()}")

# Categorías detalladas
print("\n📂 CATEGORÍAS EXISTENTES:")
for cat in Categorias.objects.all():
    count = Database.objects.filter(categoria=cat).count()
    print(f"• {cat.categoria}: {count} registros - {cat.descripcion or 'Sin descripción'}")

# Usuarios
print("\n👥 USUARIOS:")
for user in User.objects.all():
    print(f"• {user.username} ({'Administrador' if user.is_staff else 'Usuario'})")

# Ejemplos de contenido más consultado
print("\n🔥 CONTENIDO MÁS CONSULTADO (TOP 5):")
top_content = Database.objects.filter(frecuencia__gt=0).order_by('-frecuencia')[:5]
for content in top_content:
    print(f"• {content.titulo} - {content.frecuencia} consultas")

# Banners activos
print(f"\n📢 BANNERS ACTIVOS: {Banners.objects.filter(visible=True).count()}")

# Eventos próximos
from django.utils import timezone
upcoming_events = Database.objects.filter(
    evento_fecha_inicio__gte=timezone.now(),
    categoria__categoria='Calendario'
).count()
print(f"📅 EVENTOS PRÓXIMOS: {upcoming_events}")

print("\n" + "=" * 50)