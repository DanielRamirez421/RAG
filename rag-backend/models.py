from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class QueryRequest(BaseModel):
    userQuestion: str = Field(..., description="La pregunta del usuario")
    model: Literal["gpt-4o-mini", "grok-3", "DeepSeek-R1", "gpt-4o"] = Field(
        default="gpt-4o-mini", 
        description="Modelo a utilizar para generar la respuesta"
    )
    temperature: float = Field(
        default=0.7, 
        ge=0.0, 
        le=1.0, 
        description="Temperatura para la generación de texto (0-1)"
    )
    context: Optional[str] = Field(
        default=None, 
        description="Contexto o pre-prompt personalizado"
    )

class Source(BaseModel):
    chunk_id: str
    title: str
    chunk: str
    score: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    selected_model: str
    temperature: float

class ErrorResponse(BaseModel):
    error: str
    detail: str