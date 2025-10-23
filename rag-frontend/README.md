# RAG Chat Frontend

Una aplicación Angular que proporciona una interfaz de chat para interactuar con el backend RAG (Retrieval-Augmented Generation).

## Características

- **Interfaz de Chat Intuitiva**: Chat tipo conversacional con mensajes de usuario y asistente
- **Configuración de Parámetros**: Panel lateral para configurar:
  - Modelo de OpenAI (gpt-4o-mini, gpt-4, gpt-3.5-turbo)
  - Temperatura (0.0 - 2.0)
  - Contexto personalizado
- **Visualización de Fuentes**: Muestra las fuentes utilizadas por el RAG con puntajes
- **Diseño Responsivo**: Funciona en desktop y móvil
- **Material Design**: Interfaz moderna usando Angular Material

## Requisitos Previos

1. **Node.js** (v18 o superior)
2. **Backend RAG** ejecutándose en `http://localhost:8000`

## Instalación

1. **Instalar dependencias:**

   ```bash
   cd rag-frontend
   npm install
   ```

2. **Instalar Angular CLI (si no está instalado):**
   ```bash
   npm install -g @angular/cli@17
   ```

## Ejecución

1. **Asegúrate de que el backend esté ejecutándose:**

   ```bash
   # En la carpeta rag-backend
   cd ../rag-backend
   uvicorn main:app --reload
   ```

2. **Ejecutar la aplicación Angular:**

   ```bash
   cd rag-frontend
   npm start
   # o
   ng serve
   ```

3. **Abrir en el navegador:**
   ```
   http://localhost:4200
   ```

## Uso

### Configuración de Parámetros

En el panel lateral puedes configurar:

- **Modelo**: Selecciona entre los modelos de OpenAI disponibles
- **Temperatura**: Ajusta la creatividad de las respuestas (0 = muy determinista, 2 = muy creativo)
- **Contexto**: Proporciona contexto adicional para mejorar las respuestas

### Chatear

1. Escribe tu pregunta en el campo de texto
2. Presiona Enter o haz clic en el botón de enviar
3. El asistente responderá usando el sistema RAG
4. Las fuentes utilizadas se mostrarán debajo de la respuesta

### Funciones Adicionales

- **Clear Chat**: Borra toda la conversación
- **Auto-scroll**: Los mensajes se desplazan automáticamente
- **Timestamps**: Cada mensaje muestra la hora

## Estructura del Proyecto

```
src/
├── app/
│   ├── components/          # Componentes (para futuras expansiones)
│   ├── models/             # Interfaces TypeScript
│   │   └── chat.models.ts  # Modelos para chat y API
│   ├── services/           # Servicios
│   │   └── rag.service.ts  # Comunicación con la API
│   └── app.component.ts    # Componente principal
├── assets/                 # Recursos estáticos
├── styles.scss            # Estilos globales
├── index.html             # Página principal
└── main.ts               # Punto de entrada
```

## API del Backend

La aplicación se comunica con el backend RAG usando el endpoint:

```
POST /query
```

**Request Body:**

```json
{
  "userQuestion": "¿Cuál es la capital de Francia?",
  "model": "gpt-4o-mini",
  "temperature": 0.7,
  "context": "Eres un asistente útil..."
}
```

**Response:**

```json
{
  "answer": "La capital de Francia es París...",
  "selected_model": "gpt-4o-mini",
  "temperature": 0.7,
  "context": "Eres un asistente útil...",
  "sources": [
    {
      "title": "Francia - Wikipedia",
      "content": "París es la capital...",
      "score": 0.85
    }
  ]
}
```

## Desarrollo

### Scripts Disponibles

- `npm start` - Ejecutar en modo desarrollo
- `npm run build` - Construir para producción
- `npm test` - Ejecutar pruebas
- `npm run watch` - Construir y observar cambios

### Personalización

Para modificar la URL de la API, edita `src/app/services/rag.service.ts`:

```typescript
private readonly API_BASE_URL = 'http://localhost:8000'; // Cambia aquí
```

## Troubleshooting

### Problemas Comunes

1. **Error de CORS**: Asegúrate de que el backend tenga CORS habilitado
2. **Backend no disponible**: Verifica que `http://localhost:8000` esté accesible
3. **Puerto ocupado**: Angular usa el puerto 4200 por defecto

### Verificar Conexión con el Backend

```bash
curl http://localhost:8000/docs
```

Debería mostrar la documentación de la API.

## Tecnologías Utilizadas

- **Angular 17** - Framework frontend
- **Angular Material** - Componentes UI
- **TypeScript** - Lenguaje de programación
- **RxJS** - Programación reactiva
- **SCSS** - Estilos

## Próximas Mejoras

- Historial de conversaciones
- Exportar conversaciones
- Temas personalizables
- Subida de archivos para contexto
- Configuración persistente
