#!/usr/bin/env python3
from gemini_config import GeminiConfig

context = GeminiConfig.load_utc_context()
print(f"Total: {context.get('total_questions', 0)}")
print(f"Knowledge base: {len(context.get('knowledge_base', []))}")

# Buscar entradas con enlaces
entries_with_links = 0
for item in context.get('knowledge_base', []):
    if item.get('enlace_oficial'):
        entries_with_links += 1

print(f"Entries with links: {entries_with_links}")