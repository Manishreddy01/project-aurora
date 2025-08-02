from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema.document import Document
from typing import List, Tuple

# This assumes Qdrant is already populated with chunks
def run_rag_pipeline(question: str, chat_history: List[Tuple[str, str]], conversation_id: str):
    # Load vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = Qdrant(
        url="http://localhost:6333",  # or Qdrant Cloud URL
        api_key=None,  # or Qdrant Cloud API Key
        collection_name="chatbot_chunks",
        embeddings=embeddings,
    )

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "filter": {"conversationId": conversation_id}}
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=retriever,
        return_source_documents=True
    )

    result = chain({"question": question, "chat_history": chat_history})

    answer = result["answer"]
    source_docs = result["source_documents"]

    return {
        "answer": answer,
        "sources": [doc.metadata.get("source", "unknown") for doc in source_docs],
        "type": "document",
        "confidence": 0.9  # Placeholder; LangChain doesn't expose this directly
    }
