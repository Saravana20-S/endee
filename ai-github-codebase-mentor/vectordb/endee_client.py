vector_store = []

def store_embedding(embedding, metadata):

    vector_store.append({
        "embedding": embedding,
        "metadata": metadata
    })


def search_embeddings(query_embedding, top_k=5):

    import numpy as np

    scores = []

    for item in vector_store:

        score = np.dot(query_embedding, item["embedding"])
        scores.append((score, item))

    scores.sort(reverse=True)

    results = [s[1] for s in scores[:top_k]]

    return results