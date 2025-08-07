Tasks:

 Set up LangChain environment

 Configure Qdrant (local or cloud)

 Load documents using LangChain loaders

 Chunk and embed text (OpenAI / HuggingFace)

 Store vectors in Qdrant with metadata

 Create retriever (top-k with filters)

 Build ConversationalRetrievalChain (or custom RAG logic)

 Connect fallback tool (Tavily/Serper) for low-confidence responses

 Add confidence threshold logic

 Return complete response package (answer, source docs, type)


 STEPS to run this folder:
# Navigate to your working folder
cd RAG Pipeline

# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install langchain openai qdrant-client sentence-transformers unstructured pypdf python-dotenv

pip install -U langchain-community





