import chromadb
from typing import List, Dict
from chromadb.config import Settings

class VectorStore:
    def __init__(self, collection_name="sales_data", persist_path="storage/vector_db"):
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_chunks(self, chunks: List[Dict], embeddings: List[List[float]]):
        self.collection.add(
            documents=[chunk["text"] for chunk in chunks],
            embeddings=embeddings,
            metadatas=[chunk["metadata"] for chunk in chunks],
            ids=[chunk["chunk_id"] for chunk in chunks]
        )

    def query(self, query_embedding: List[float], top_k=3):
        return self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
