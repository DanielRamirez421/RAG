#!/usr/bin/env python3

"""
Script para verificar las importaciones disponibles de Azure Search Documents
"""

print("Verificando importaciones de Azure Search Documents...")

# Verificar versión
try:
    import azure.search.documents
    print(f"✅ azure.search.documents version: {azure.search.documents.__version__}")
except:
    print("❌ No se pudo importar azure.search.documents")

# Verificar VectorizableTextQuery
try:
    from azure.search.documents.models import VectorizableTextQuery
    print("✅ VectorizableTextQuery disponible en azure.search.documents.models")
except ImportError as e:
    print(f"❌ VectorizableTextQuery no disponible en models: {e}")
    
    try:
        from azure.search.documents import VectorizableTextQuery
        print("✅ VectorizableTextQuery disponible en azure.search.documents")
    except ImportError as e:
        print(f"❌ VectorizableTextQuery no disponible: {e}")

# Verificar otras importaciones necesarias
try:
    from azure.search.documents.models import VectorizedQuery
    print("✅ VectorizedQuery disponible")
except ImportError:
    print("❌ VectorizedQuery no disponible")

# Listar todos los modelos disponibles
try:
    import azure.search.documents.models as models
    available_models = [attr for attr in dir(models) if not attr.startswith('_')]
    print(f"\n📋 Modelos disponibles en azure.search.documents.models:")
    for model in sorted(available_models):
        print(f"   - {model}")
except Exception as e:
    print(f"❌ Error listando modelos: {e}")

print("\n🔍 Verificación completada.")