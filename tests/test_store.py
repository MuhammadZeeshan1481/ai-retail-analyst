import sys
import os
sys.path.append(os.path.abspath("."))

from backend.embedding_engine import EmbeddingEngine
from backend.vector_store import VectorStore
from backend.file_parser import read_file, chunk_dataframe

# Step 1: Load and chunk
df = read_file("data/uploads/sample_sales.csv")
chunks = chunk_dataframe(df)

# Step 2: Generate embeddings
embedder = EmbeddingEngine()
embeddings = embedder.embed_texts([c["text"] for c in chunks])

# Step 3: Store into Chroma
store = VectorStore()
store.add_chunks(chunks, embeddings)

print(f" Stored {len(chunks)} chunks in Chroma vector DB.")
