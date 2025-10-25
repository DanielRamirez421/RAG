#!/usr/bin/env python3
"""
Script de prueba para verificar que todas las dependencias y configuraciones
funcionan correctamente en Railway
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Probar que todas las variables de entorno están configuradas"""
    print("🔍 Verificando variables de entorno...")
    
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT", 
        "OPENAI_API_VERSION",
        "AZURE_SEARCH_SERVICE_ENDPOINT",
        "AZURE_SEARCH_INDEX",
        "AZURE_SEARCH_ADMIN_KEY"
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
            print(f"❌ {var}: NOT SET")
        else:
            print(f"✅ {var}: SET")
    
    if missing:
        print(f"\n🚨 Variables faltantes: {', '.join(missing)}")
        return False
    
    print("\n✅ Todas las variables de entorno están configuradas")
    return True

def test_imports():
    """Probar que todas las dependencias se pueden importar"""
    print("\n🔍 Verificando imports...")
    
    try:
        from fastapi import FastAPI
        print("✅ FastAPI")
        
        from openai import AzureOpenAI
        print("✅ Azure OpenAI")
        
        from azure.search.documents import SearchClient
        print("✅ Azure Search")
        
        from azure.core.credentials import AzureKeyCredential
        print("✅ Azure Credentials")
        
        import dotenv
        print("✅ Python dotenv")
        
        print("\n✅ Todas las dependencias se importaron correctamente")
        return True
        
    except Exception as e:
        print(f"\n❌ Error importando dependencias: {e}")
        return False

def test_azure_connections():
    """Probar conexiones básicas a Azure"""
    print("\n🔍 Verificando conexiones a Azure...")
    
    try:
        from openai import AzureOpenAI
        
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("OPENAI_API_VERSION")
        )
        
        print("✅ Cliente Azure OpenAI inicializado")
        
        from azure.search.documents import SearchClient
        from azure.core.credentials import AzureKeyCredential
        
        search_client = SearchClient(
            endpoint=os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT"),
            index_name=os.getenv("AZURE_SEARCH_INDEX"),
            credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_ADMIN_KEY"))
        )
        
        print("✅ Cliente Azure Search inicializado")
        print("\n✅ Conexiones a Azure configuradas correctamente")
        return True
        
    except Exception as e:
        print(f"\n❌ Error conectando a Azure: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de Railway...\n")
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Ejecutar pruebas
    tests = [
        test_environment,
        test_imports,
        test_azure_connections
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 ¡Todas las pruebas pasaron! La aplicación debería funcionar en Railway.")
        sys.exit(0)
    else:
        print("❌ Algunas pruebas fallaron. Revisa la configuración.")
        sys.exit(1)