import requests
import json

# URL base de la API
BASE_URL = "http://localhost:8000"

def test_health():
    """Probar el endpoint de salud"""
    response = requests.get(f"{BASE_URL}/health")
    print("=== Test Health ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_models():
    """Probar el endpoint de modelos disponibles"""
    response = requests.get(f"{BASE_URL}/models")
    print("=== Test Models ===")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_query(question="Nitrogen fertilization is important for?", 
               model="gpt-4o-mini", 
               temperature=0.7, 
               context=None):
    """Probar el endpoint principal de consulta"""
    payload = {
        "userQuestion": question,
        "model": model,
        "temperature": temperature
    }
    
    if context:
        payload["context"] = context
    
    response = requests.post(
        f"{BASE_URL}/query",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    
    print("=== Test Query ===")
    print(f"Question: {question}")
    print(f"Model: {model}")
    print(f"Temperature: {temperature}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Answer: {result['answer']}")
        print(f"Sources found: {len(result['sources'])}")
        for i, source in enumerate(result['sources']):
            print(f"  Source {i+1}: {source['title']} (Score: {source['score']:.3f})")
    else:
        print(f"Error: {response.text}")
    print()

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 Probando RAG Backend API...\n")
    
    try:
        # Probar salud
        test_health()
        
        # Probar modelos
        test_models()
        
        # Probar consulta básica
        test_query()
        
        # Probar con contexto personalizado
        test_query(
            question="¿Qué es la fertilización con nitrógeno?",
            context="Eres un experto en agricultura. Responde de manera técnica y precisa."
        )
        
        # Probar con diferente modelo y temperatura
        test_query(
            question="How does nitrogen affect plant growth?",
            model="gpt-4o",
            temperature=0.2
        )
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor.")
        print("Asegúrate de que el servidor esté ejecutándose en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()