from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Optional print checks
print("🔑 OpenAI API Key:", os.getenv("OPENAI_API_KEY")[:5] + "..." if os.getenv("OPENAI_API_KEY") else "Not set")
print("🔑 Qdrant URL:", os.getenv("QDRANT_URL") or "Not set")
print("🔑 HuggingFace Token:", os.getenv("HUGGINGFACEHUB_API_TOKEN")[:5] + "..." if os.getenv("HUGGINGFACEHUB_API_TOKEN") else "Not set")
print("🔍 Tavily API Key:", os.getenv("TAVILY_API_KEY")[:5] + "..." if os.getenv("TAVILY_API_KEY") else "Not set")

# Placeholder for next steps
def main():
    print("\n✅ RAG pipeline environment is ready.")
    # We'll add loaders, embeddings, vectorstore, and retrieval here.

if __name__ == "__main__":
    main()
