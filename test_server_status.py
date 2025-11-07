#!/usr/bin/env python3
"""
Script para verificar el estado del servidor Django y probar FALCON
"""

import requests
import json

def test_server_connection():
    """Probar conexión al servidor Django"""
    try:
        print("🔍 Probando conexión al servidor Django...")
        
        # Probar página principal
        response = requests.get('http://127.0.0.1:8000/', timeout=5)
        
        if response.status_code == 200:
            print("✅ Servidor Django funcionando correctamente")
            print(f"   Status Code: {response.status_code}")
            return True
        else:
            print(f"⚠️  Servidor responde con código: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor")
        print("   Verifica que Django esté corriendo en http://127.0.0.1:8000/")
        return False
    except requests.exceptions.Timeout:
        print("❌ Error: Timeout al conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def test_chatbot_endpoint():
    """Probar endpoint del chatbot"""
    try:
        print("\n🤖 Probando endpoint del chatbot...")
        
        # Datos de prueba
        test_data = {
            'message': 'hola'
        }
        
        # Headers necesarios
        headers = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        # Hacer petición POST
        response = requests.post(
            'http://127.0.0.1:8000/chatbot/',
            json=test_data,
            headers=headers,
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print("✅ Chatbot funcionando correctamente")
                print(f"   Respuesta: {result.get('response', 'Sin respuesta')}")
                return True
            except json.JSONDecodeError:
                print("⚠️  Respuesta no es JSON válido")
                print(f"   Contenido: {response.text[:200]}...")
        else:
            print(f"❌ Error en chatbot: {response.status_code}")
            print(f"   Contenido: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Error al probar chatbot: {str(e)}")
        
    return False

def main():
    """Función principal"""
    print("🚀 VERIFICANDO ESTADO DEL SERVIDOR FALCON")
    print("=" * 50)
    
    # Probar conexión básica
    server_ok = test_server_connection()
    
    if server_ok:
        # Probar chatbot
        chatbot_ok = test_chatbot_endpoint()
        
        if chatbot_ok:
            print("\n🎉 ¡TODO FUNCIONANDO CORRECTAMENTE!")
        else:
            print("\n⚠️  Servidor OK, pero hay problemas con el chatbot")
    else:
        print("\n❌ PROBLEMAS DE CONECTIVIDAD CON EL SERVIDOR")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()