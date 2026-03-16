# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer("all-MiniLM-L6-v2")

# def generate_embedding(text):

#     return model.encode(text).tolist()


from sentence_transformers import SentenceTransformer
import json
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(chunks):

    embeddings = model.encode(chunks).tolist()

    os.makedirs("data/embeddings", exist_ok=True)

    data = []

    for chunk, vector in zip(chunks, embeddings):
        data.append({
            "text": chunk,
            "embedding": vector
        })

    with open("data/embeddings/embeddings.json", "w") as f:
        json.dump(data, f)

    print(f"Saved {len(data)} embeddings")

    return embeddings