import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.get_or_create_collection("memory", embedding_function=embedding_function)

def store_memory(text: str, source: str = "assistant"):
    collection.add(
        documents=[text],
        ids=[f"{source}_{len(collection.get()['ids'])}"],
        metadatas=[{"source": source}]
    )
    print(f"[🧠 Stored memory from {source}]")

def recall_memory(query: str, top_k: int = 3):
    results = collection.query(query_texts=[query], n_results=top_k)
    return results["documents"][0] if results["documents"] else []
