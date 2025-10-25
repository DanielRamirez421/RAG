from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import QueryRequest, QueryResponse, ErrorResponse
from rag_service import RAGService
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear la aplicación FastAPI
app = FastAPI(
    title="RAG Backend API",
    description="API para consultar la base de conocimiento usando RAG (Retrieval-Augmented Generation)",
    version="1.0.0"
)

# Configurar CORS para producción
allowed_origins = [
    "http://localhost:4200",  # Frontend local
    "http://localhost:3000",  # React local
    "http://localhost:8080",  # Otros puertos locales
    "http://127.0.0.1:3000",  # Localhost alternativo
    "https://tu-frontend-deploy.vercel.app",  # Frontend desplegado
    "https://*.up.railway.app",  # Railway domains
    "https://*.railway.app",     # Railway custom domains
    "https://*.vercel.app",      # Vercel domains
    "https://*.netlify.app",     # Netlify domains
    "https://*.github.io",       # GitHub Pages
    # Agregar más dominios según sea necesario
]

# En desarrollo, permitir todos los orígenes
if os.getenv("ENVIRONMENT") == "development":
    allowed_origins = ["*"]

# Para permitir CUALQUIER origen (usar con precaución en producción)
if os.getenv("ALLOW_ALL_ORIGINS") == "true":
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Inicializar el servicio RAG con manejo de errores
try:
    # Log environment variables for debugging (without showing sensitive values)
    logger.info("Checking environment variables...")
    env_check = {
        "AZURE_OPENAI_API_KEY": "SET" if os.getenv("AZURE_OPENAI_API_KEY") else "MISSING",
        "AZURE_OPENAI_ENDPOINT": "SET" if os.getenv("AZURE_OPENAI_ENDPOINT") else "MISSING",
        "OPENAI_API_VERSION": "SET" if os.getenv("OPENAI_API_VERSION") else "MISSING",
        "AZURE_SEARCH_SERVICE_ENDPOINT": "SET" if os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT") else "MISSING",
        "AZURE_SEARCH_INDEX": "SET" if os.getenv("AZURE_SEARCH_INDEX") else "MISSING",
        "AZURE_SEARCH_ADMIN_KEY": "SET" if os.getenv("AZURE_SEARCH_ADMIN_KEY") else "MISSING",
    }
    
    missing_vars = [k for k, v in env_check.items() if v == "MISSING"]
    if missing_vars:
        logger.error(f"Missing environment variables: {missing_vars}")
        logger.error("Please set these variables in Railway's Variables tab")
    else:
        logger.info("All environment variables are set")
    
    rag_service = RAGService()
    logger.info("RAG Service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize RAG Service: {str(e)}")
    logger.error("This usually means environment variables are not set correctly in Railway")
    rag_service = None

@app.get("/")
async def root():
    """Endpoint de salud de la API"""
    return {"message": "RAG Backend API está funcionando correctamente"}

@app.get("/health")
async def health_check():
    """Verificar el estado de la API"""
    health_status = {
        "status": "healthy",
        "service": "RAG Backend",
        "rag_service_initialized": rag_service is not None
    }
    
    if rag_service is None:
        health_status["status"] = "unhealthy"
        health_status["error"] = "RAG Service not initialized"
        
    return health_status

@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Endpoint principal para hacer consultas RAG
    
    - **userQuestion**: La pregunta que quieres hacer a la base de conocimiento
    - **model**: El modelo de IA a utilizar (gpt-4o-mini, grok-3, DeepSeek-R1, gpt-4o)
    - **temperature**: Controla la creatividad de la respuesta (0.0 = más determinista, 1.0 = más creativo)
    - **context**: Contexto personalizado o pre-prompt (opcional)
    """
    if rag_service is None:
        raise HTTPException(
            status_code=503,
            detail="RAG Service is not available. Check environment variables and Azure connections."
        )
    
    try:
        logger.info(f"Procesando consulta: {request.userQuestion}")
        logger.info(f"Modelo: {request.model}, Temperatura: {request.temperature}")
        
        result = rag_service.generate_answer(
            user_question=request.userQuestion,
            model=request.model,
            temperature=request.temperature,
            context=request.context
        )
        
        logger.info("Consulta procesada exitosamente")
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"Error procesando consulta: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.get("/models")
async def get_available_models():
    """Obtener la lista de modelos disponibles"""
    return {
        "models": ["gpt-4o-mini", "grok-3", "DeepSeek-R1", "gpt-4o"],
        "default": "gpt-4o-mini"
    }

@app.get("/debug/env")
async def debug_environment():
    """Debug endpoint para verificar variables de entorno (solo en desarrollo)"""
    env_vars = {
        "AZURE_SEARCH_SERVICE_ENDPOINT": os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT", "NOT_SET"),
        "AZURE_SEARCH_INDEX": os.getenv("AZURE_SEARCH_INDEX", "NOT_SET"),
        "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT", "NOT_SET"),
        "OPENAI_API_VERSION": os.getenv("OPENAI_API_VERSION", "NOT_SET"),
        "PORT": os.getenv("PORT", "NOT_SET"),
        "ENVIRONMENT": os.getenv("ENVIRONMENT", "NOT_SET"),
        # No mostrar claves por seguridad
        "AZURE_SEARCH_ADMIN_KEY": "SET" if os.getenv("AZURE_SEARCH_ADMIN_KEY") else "NOT_SET",
        "AZURE_OPENAI_API_KEY": "SET" if os.getenv("AZURE_OPENAI_API_KEY") else "NOT_SET",
    }
    return {"environment_variables": env_vars}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Cambiar a False para producción
        log_level="info"
    )