# 🧠 Proyecto RAG - Planeación Inteligente de Cultivos

Este proyecto conecta con el servicio **Azure AI Projects** para ejecutar un agente inteligente de conversación (RAG-PLA) dedicado a la _Planeación Inteligente de Cultivos_.

---

## 🚀 1. Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener instalados los siguientes componentes:

- **Node.js** v18 o superior (recomendado v20+)
- **Azure CLI**
- Acceso a un **AI Project** configurado en Azure
- Permisos de rol: _Cognitive Services OpenAI User_ o superior

Verifica tus versiones:

```bash
node -v
az version
```

---

## ⚙️ 2. Instalación

1. Instala las dependencias:

   ```bash
   npm install
   ```

2. Inicia sesión en Azure:
   ```bash
   az login
   az account show
   ```

---

## ▶️ 3. Ejecución

Ejecuta el agente conversacional con:

```bash
node runAgentConversation.js
```

o directamente:

```bash
npm start
```

---

## 🧾 5. Descripción del script principal

El archivo `runAgentConversation.js` realiza los siguientes pasos:

1. **Conecta** con el proyecto de Azure AI a través de `AIProjectClient`.
2. **Recupera** el agente RAG-PLA definido en Azure.
3. **Crea un hilo** de conversación (`thread`).
4. **Envía un mensaje** inicial desde el usuario.
5. **Ejecuta** el _run_ del agente hasta obtener respuesta.
6. **Muestra** los mensajes resultantes en consola.

---

## ⚠️ 6. Solución de errores comunes

| Error                                               | Causa                                | Solución                                       |
| --------------------------------------------------- | ------------------------------------ | ---------------------------------------------- |
| `DefaultAzureCredential failed to retrieve a token` | No se inició sesión en Azure         | Ejecuta `az login`                             |
| `403 Forbidden`                                     | Falta de permisos sobre el proyecto  | Asigna el rol “Cognitive Services OpenAI User” |
| `Run failed`                                        | ID de agente incorrecto o sin acceso | Verifica el ID en el portal de Azure           |

---

## 📂 7. Estructura del proyecto

```
topicos-rag/
├── .git/
├── .gitignore
├── node_modules/
├── package.json
├── package-lock.json
└── runAgentConversation.js
```

---

## 👨‍💻 8. Autor

**Daniel Mauricio Ramírez Castaño**  
Proyecto final - _Tópicos Avanzados de Desarrollo de Software (EAFIT)_  
Universidad EAFIT - 2025
