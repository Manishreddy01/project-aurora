Tasks:

 Set up backend server (choose FastAPI or Node.js)

 Route 1: POST /upload → Receive files or pasted text, send to n8n

 Route 2: POST /query → Accept user query, trigger vector search + LLM

 Route 3: Health check, logs, etc.

 Integrate with LangChain pipeline (RAG logic)

 Handle fallback search (Serper/Tavily)

 Return formatted responses to frontend