

from vectordb.endee_client import search_embeddings, vector_store
from embeddings.embedding_model import generate_embeddings
from config.settings import TOP_K_RESULTS

def retrieve_context(question):
    """
    Retrieve relevant code chunks from Endee vector DB or local fallback.
    Returns a list of code chunks and prints debug info.
    """
    context_chunks = []

    try:
        # Step 1: Convert question → embedding
        query_embedding = generate_embeddings([question])[0]
        print("Query embedding generated")

        # Step 2: Search embeddings
        results = search_embeddings(query_embedding, top_k=TOP_K_RESULTS)
        print("Results fetched:", len(results))

        # Step 3: Process results
        for i, r in enumerate(results):
            if isinstance(r, dict):
                meta = r.get("metadata", {})
                code = meta.get("code", "")
                filename = meta.get("file", "unknown")
            else:
                code = r
                filename = f"local_{i}"

            if code.strip():
                context_chunks.append({
                    "file": filename,
                    "code": code
                })

        # Step 4: Fallback if nothing found
        if not context_chunks:
            print("⚠️ No relevant context found from vector DB or local store")
            for i, item in enumerate(vector_store[:TOP_K_RESULTS]):
                if isinstance(item, dict):
                    code = item.get("metadata", {}).get("code", "")
                    filename = item.get("metadata", {}).get("file", f"local_{i}")
                else:
                    code = item
                    filename = f"local_{i}"

                if code.strip():
                    context_chunks.append({
                        "file": filename,
                        "code": code
                    })

        return context_chunks

    except Exception as e:
        print("❌ Error in retrieve_context:", e)
        return []