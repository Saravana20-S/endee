# test_storage.py
from embeddings.embedding_model import embedder
from vectordb.endee_client import endee_client
import time

# 1. New Index
idx_name = f"test_bare_{int(time.time()) % 1000}"
print(f"--- Creating Index: {idx_name} ---")
print(endee_client.create_index(idx_name))

# 2. Vectorize
text = ["Testing bare insert"]
vectors = embedder.generate_embeddings(text)

# 3. Insert (Bare)
print(f"\n--- Inserting Bare Vector ---")
res = endee_client.insert_vectors(idx_name, vectors, [])
print(f"Insert Response: {res}")

# 4. Search
if res.get('status_code') == 200:
    print(f"\n--- Searching ---")
    print(endee_client.search_vectors(idx_name, vectors[0], k=1))