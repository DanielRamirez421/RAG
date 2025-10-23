from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import QueryRequest, QueryResponse, ErrorResponse
from rag_service import RAGService
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear la aplicación FastAPI
app = FastAPI(
    title="RAG Backend API",
    description="API para consultar la base de conocimiento usando RAG (Retrieval-Augmented Generation)",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar el servicio RAG
rag_service = RAGService()

@app.get("/")
async def root():
    """Endpoint de salud de la API"""
    return {"message": "RAG Backend API está funcionando correctamente"}

@app.get("/health")
async def health_check():
    """Verificar el estado de la API"""
    return {"status": "healthy", "service": "RAG Backend"}

@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Endpoint principal para hacer consultas RAG
    
    - **userQuestion**: La pregunta que quieres hacer a la base de conocimiento
    - **model**: El modelo de IA a utilizar (gpt-4o-mini, grok-3, DeepSeek-R1, gpt-4o)
    - **temperature**: Controla la creatividad de la respuesta (0.0 = más determinista, 1.0 = más creativo)
    - **context**: Contexto personalizado o pre-prompt (opcional)
    """
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )