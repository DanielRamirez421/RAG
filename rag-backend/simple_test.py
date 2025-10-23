#!/usr/bin/env python3

import requests
import json

# Configuración
API_URL = "http://localhost:8000"

def test_simple_query():
    """Prueba básica de la API con el ejemplo del usuario"""
    
    # Datos correctamente formateados
    payload = {
        "userQuestion": "¿Qué es importante sobre la fertilización con nitrógeno?",
        "model": "gpt-4o-mini",
        "temperature": 0.7
    }
    
    print("🚀 Probando la API RAG...")
    print(f"📝 Pregunta: {payload['userQuestion']}")
    print(f"🤖 Modelo: {payload['model']}")
    print(f"🌡️ Temperatura: {payload['temperature']}")
    print("-" * 50)
    
    try:
        response = requests.post(
            f"{API_URL}/query",
            headers={"Content-Type": "application/json"},
            json=payload  # Usar json= en lugar de data=
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ ¡Respuesta exitosa!")
            print(f"💬 Respuesta: {result['answer']}")
            print(f"🔍 Fuentes encontradas: {len(result['sources'])}")
            
            for i, source in enumerate(result['sources'], 1):
                print(f"   📚 Fuente {i}: {source['title'][:50]}...")
                print(f"      Score: {source['score']:.3f}")
            
            print(f"🤖 Modelo usado: {result['selected_model']}")
            print(f"🌡️ Temperatura: {result['temperature']}")
            
        else:
            print("❌ Error en la respuesta:")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor.")
        print("Asegúrate de que el servidor esté ejecutándose en http://localhost:8000")
        print("Ejecuta: python3 main.py")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_simple_query()