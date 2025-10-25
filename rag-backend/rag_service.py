import os
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery
import dotenv

# Cargar variables de entorno
dotenv.load_dotenv()

class RAGService:
    def __init__(self):
        # Configuración de Azure OpenAI
        self.azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.openai_api_version = os.getenv("OPENAI_API_VERSION")
        self.embedding_model = "text-embedding-ada-002"
        
        # Configuración de Azure Search
        self.azure_search_endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
        self.azure_search_index = os.getenv("AZURE_SEARCH_INDEX")
        self.azure_search_key = os.getenv("AZURE_SEARCH_ADMIN_KEY")
        
        # Validar que todas las variables de entorno estén configuradas
        required_vars = {
            "AZURE_OPENAI_API_KEY": self.azure_openai_api_key,
            "AZURE_OPENAI_ENDPOINT": self.azure_openai_endpoint,
            "OPENAI_API_VERSION": self.openai_api_version,
            "AZURE_SEARCH_SERVICE_ENDPOINT": self.azure_search_endpoint,
            "AZURE_SEARCH_INDEX": self.azure_search_index,
            "AZURE_SEARCH_ADMIN_KEY": self.azure_search_key,
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Inicializar clientes
        try:
            self.openai_client = AzureOpenAI(
                api_key=self.azure_openai_api_key,
                azure_endpoint=self.azure_openai_endpoint,
                api_version=self.openai_api_version
            )
            
            self.search_client = SearchClient(
                endpoint=self.azure_search_endpoint,
                index_name=self.azure_search_index,
                credential=AzureKeyCredential(self.azure_search_key)
            )
        except Exception as e:
            raise ValueError(f"Failed to initialize Azure clients: {str(e)}")
    
    def get_embedding(self, text: str):
        """Obtiene el embedding de un texto usando Azure OpenAI"""
        return self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=text
        ).data[0].embedding
    
    def search_documents(self, query: str, top_k: int = 3):
        """Busca documentos relevantes en Azure Search"""
        try:
            # Obtener el embedding del query
            query_vector = self.get_embedding(query)
            
            # Usar VectorizedQuery con el vector calculado
            search_results = self.search_client.search(
                search_text=None,
                top=top_k,
                vector_queries=[
                    VectorizedQuery(
                        vector=query_vector,
                        k_nearest_neighbors=top_k,
                        fields="text_vector"
                    )
                ]
            )
        except Exception as e:
            # Fallback a búsqueda de texto simple
            print(f"Vector search failed, falling back to text search: {e}")
            search_results = self.search_client.search(
                search_text=query,
                top=top_k
            )
        
        results = []
        for result in search_results:
            results.append({
                "chunk_id": result.get("chunk_id", ""),
                "title": result.get("title", ""),
                "chunk": result.get("chunk", ""),
                "score": result.get("@search.score", 0)
            })
        
        return results
    
    def generate_answer(self, user_question: str, model: str, temperature: float, context: str = None):
        """Genera una respuesta usando RAG"""
        try:
            # Buscar documentos relevantes
            search_results = self.search_documents(user_question)
            
            # Construir contexto de los resultados de búsqueda
            retrieved_context = ""
            for result in search_results:
                retrieved_context += result["chunk"] + "\n\n"
            
            # Usar el contexto proporcionado o el predeterminado
            if context:
                system_message = f"""
{context}

Context from knowledge base:
{retrieved_context}
"""
            else:
                system_message = f"""
You are an AI Assistant.
Be brief in your answers. Answer ONLY with the facts listed in the retrieved text.

Context:
{retrieved_context}
"""
            
            # Generar respuesta
            response = self.openai_client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_question},
                ],
            )
            
            answer = response.choices[0].message.content
            
            return {
                "answer": answer,
                "sources": search_results,
                "selected_model": model,
                "temperature": temperature
            }
            
        except Exception as e:
            raise Exception(f"Error generating answer: {str(e)}")