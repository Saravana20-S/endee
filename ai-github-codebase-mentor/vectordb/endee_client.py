import uuid
import numpy as np

# Try importing Endee
try:
    from endee import Endee
    client = Endee()
    ENDEE_AVAILABLE = True
except Exception as e:
    print("⚠️ Endee not available, switching to local vector DB")
    ENDEE_AVAILABLE = False

INDEX_NAME = "github-codebase"
DIMENSION = 384  # all-MiniLM-L6-v2

# Fallback local store
vector_store = []

def get_or_create_index():
    try:
        indexes = client.list_indexes()
        index_names = [idx["name"] for idx in indexes]

        if INDEX_NAME not in index_names:
            print("📦 Creating Endee index...")
            client.create_index(
                name=INDEX_NAME,
                dimension=DIMENSION,
                space_type="cosine"
            )
        return client.get_index(INDEX_NAME)
    except Exception as e:
        print("❌ Endee connection failed:", e)
        return None

def normalize(vec):
    return vec / np.linalg.norm(vec)

def store_embedding(embedding, metadata):
    embedding = normalize(np.array(embedding))

    if ENDEE_AVAILABLE:
        index = get_or_create_index()
        if index:
            try:
                index.upsert([{
                    "id": str(uuid.uuid4()),
                    "vector": embedding.tolist(),
                    "meta": metadata
                }])
                print(f"✅ Stored in Endee: {metadata.get('file','unknown')}")
                return
            except Exception as e:
                print("❌ Endee store failed, using fallback:", e)

    # Fallback
    vector_store.append({
        "embedding": embedding,
        "metadata": metadata
    })
    print(f"💾 Stored locally: {metadata.get('file','unknown')}")

def store_embeddings_batch(embeddings, metadatas):
    embeddings = [normalize(np.array(e)) for e in embeddings]

    if ENDEE_AVAILABLE:
        index = get_or_create_index()
        if index:
            try:
                batch = [{"id": str(uuid.uuid4()), "vector": e.tolist(), "meta": m} for e, m in zip(embeddings, metadatas)]
                index.upsert(batch)
                print(f"✅ Stored batch of {len(batch)} embeddings in Endee")
                return
            except Exception as e:
                print("❌ Endee batch store failed, using fallback:", e)

    # Fallback local
    for e, m in zip(embeddings, metadatas):
        vector_store.append({
            "embedding": e,
            "metadata": m
        })
    print(f"💾 Stored batch of {len(embeddings)} embeddings locally")

def search_embeddings(query_embedding, top_k=5):
    """Return consistent dicts for Streamlit"""
    query_embedding = normalize(np.array(query_embedding))

    # Endee search
    if ENDEE_AVAILABLE:
        index = get_or_create_index()
        if index:
            try:
                raw_results = index.query(vector=query_embedding.tolist(), top_k=top_k)
                results = []
                for r in raw_results:
                    results.append({
                        "embedding": r.get("vector"),
                        "metadata": r.get("meta") if isinstance(r.get("meta"), dict) else {}
                    })
                return results
            except Exception as e:
                print("❌ Endee search failed, using fallback:", e)

    # Local fallback search
    scores = []
    for item in vector_store:
        if not isinstance(item, dict):
            continue  # skip invalid
        metadata = item.get("metadata", {}) if isinstance(item.get("metadata"), dict) else {}
        score = np.dot(query_embedding, item["embedding"])
        scores.append((score, {"embedding": item["embedding"], "metadata": metadata}))
    scores.sort(key=lambda x: x[0], reverse=True)
    return [s[1] for s in scores[:top_k]]

