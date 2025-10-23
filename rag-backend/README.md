# RAG Backend API

API backend para consultar una base de conocimiento usando RAG (Retrieval-Augmented Generation) con Azure OpenAI y Azure Search.

## Instalación

1. **Crear entorno virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # En macOS/Linux
   # venv\Scripts\activate     # En Windows
   ```

2. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Edita el archivo .env con tus credenciales de Azure
   ```

## Configuración

Asegúrate de configurar las siguientes variables en tu archivo `.env`:

- `AZURE_OPENAI_API_KEY`: Tu clave de API de Azure OpenAI
- `AZURE_OPENAI_ENDPOINT`: El endpoint de tu servicio Azure OpenAI
- `OPENAI_API_VERSION`: Versión de la API (ej: 2023-05-15)
- `AZURE_SEARCH_SERVICE_ENDPOINT`: Endpoint de tu servicio Azure Search
- `AZURE_SEARCH_INDEX`: Nombre de tu índice de búsqueda
- `AZURE_SEARCH_ADMIN_KEY`: Clave de administrador de Azure Search

## Uso

### Ejecutar el servidor

```bash
python main.py
```

O usando uvicorn directamente:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

El servidor estará disponible en: http://localhost:8000

### Documentación de la API

Una vez que el servidor esté ejecutándose, puedes acceder a:

- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

## Endpoints

### POST /query

Endpoint principal para hacer consultas RAG.

**Parámetros:**

- `userQuestion` (string, requerido): La pregunta para la base de conocimiento
- `model` (string, opcional): Modelo a usar ["gpt-4o-mini", "grok-3", "DeepSeek-R1", "gpt-4o"]
- `temperature` (float, opcional): Temperatura para la generación (0.0-1.0)
- `context` (string, opcional): Contexto personalizado o pre-prompt

**Ejemplo de request:**

```json
{
  "userQuestion": "¿Qué es la fertilización con nitrógeno?",
  "model": "gpt-4o-mini",
  "temperature": 0.7,
  "context": "Eres un experto en agricultura. Responde de manera técnica y precisa."
}
```

**Ejemplo de response:**

```json
{
  "answer": "La fertilización con nitrógeno es...",
  "sources": [
    {
      "chunk_id": "doc_1_chunk_1",
      "title": "Fertilización en Agricultura",
      "chunk": "Texto del documento relevante...",
      "score": 0.85
    }
  ],
  "selected_model": "gpt-4o-mini",
  "temperature": 0.7
}
```

### GET /models

Obtiene la lista de modelos disponibles.

### GET /health

Verifica el estado de la API.

## Ejemplo de uso con curl

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "userQuestion": "¿Qué es importante sobre la fertilización con nitrógeno?",
       "model": "gpt-4o-mini",
       "temperature": 0.7
     }'
```

## Estructura del proyecto

```
rag-backend/
├── main.py              # Aplicación FastAPI principal
├── rag_service.py       # Servicio RAG con Azure OpenAI y Search
├── models.py            # Modelos Pydantic para requests/responses
├── requirements.txt     # Dependencias
├── .env.example         # Ejemplo de variables de entorno
└── README.md           # Esta documentación
```
