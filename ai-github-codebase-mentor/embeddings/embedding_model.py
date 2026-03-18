


# embeddings/embedding_model.py
from sentence_transformers import SentenceTransformer
from config.settings import settings

class Embedder:
    def __init__(self):
        
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

    def generate_embeddings(self, text_list):
        """Converts a list of strings into a list of vectors."""
        print(f"Generating embeddings for {len(text_list)} chunks...")
        embeddings = self.model.encode(text_list)
        
        return [vec.tolist() for vec in embeddings]

embedder = Embedder()