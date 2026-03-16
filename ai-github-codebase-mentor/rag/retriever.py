from vectordb.endee_client import search_embeddings
from embeddings.embedding_model import generate_embeddings
from config.settings import TOP_K_RESULTS

def retrieve_context(question):

    query_embedding = generate_embeddings(question)

    results = search_embeddings(query_embedding, TOP_K_RESULTS)

    context = ""

    for r in results:

        context += r["metadata"]["code"] + "\n"

    return context