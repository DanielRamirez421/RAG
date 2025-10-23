#!/bin/bash

# Script para configurar y ejecutar el backend RAG

echo "🔧 Configurando RAG Backend..."

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado. Copiando desde .env.example..."
    cp .env.example .env
    echo "✏️  Por favor, edita el archivo .env con tus credenciales de Azure."
    exit 1
fi

echo "✅ Configuración completada!"
echo ""
echo "🚀 Para ejecutar el servidor:"
echo "   python main.py"
echo ""
echo "📖 Para ver la documentación:"
echo "   http://localhost:8000/docs"
echo ""
echo "🧪 Para probar la API:"
echo "   python test_api.py"