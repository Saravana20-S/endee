


# services/pipeline.py
from ingestion.clone_repo import clone_repository
from ingestion.extract_files import get_code_files
from ingestion.chunk_code import process_repo_into_chunks
from embeddings.embedding_model import embedder
from vectordb.endee_client import endee_client
from rag.generator import generator
import time

class GitHubMentorPipeline:
    def __init__(self, index_name):
        self.index_name = index_name

    def ingest_new_repo(self, repo_url):
        """Full pipeline: Clone -> Extract -> Chunk -> Embed -> Store."""
        print(f"--- Starting Ingestion for {repo_url} ---")
        
        # 1. Clone
        repo_path = clone_repository(repo_url)
        
        # 2. Extract & Chunk
        files = get_code_files(repo_path)
        chunks_data = process_repo_into_chunks(files)
        
        # 3. Create Index
        print(f"Creating Index: {self.index_name}")
        endee_client.create_index(self.index_name)
        time.sleep(2) # Buffer for DB initialization
        
        # 4. Embed & Store
        texts = [c['text'] for c in chunks_data]
        metas = [c['metadata'] for c in chunks_data]
        
        # We batch embeddings to avoid overloading memory
        batch_size = 50
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_metas = metas[i:i+batch_size]
            
            vectors = embedder.generate_embeddings(batch_texts)
            endee_client.insert_vectors(self.index_name, vectors, batch_metas)
            print(f"Indexed batch {i//batch_size + 1}")

        print(f"✅ Successfully indexed {len(chunks_data)} chunks.")

    # services/pipeline.py (Update the ask_question method)

    def ask_question(self, question):
        """Retrieval Augmented Generation loop."""
        # 1. Embed the question
        query_vector = embedder.generate_embeddings([question])[0]
        
        # 2. Retrieve from Endee
        search_res = endee_client.search_vectors(self.index_name, query_vector, k=4)
        
        # 3. Parse the Results
        context = []
        # If Endee returns a list of results in 'raw_body' or 'results'
        # We need to extract the 'meta' -> 'title' (which we stored as the file content)
        if isinstance(search_res, list):
            for item in search_res:
                # Based on our insert, content is in meta['title']
                content = item.get('meta', {}).get('title', "")
                if content:
                    context.append(content)
        
        # fallback for our test if retrieval fails
        if not context:
            context = ["No specific code found, but here is a general analysis..."]
        
        # 4. Generate Answer
        return generator.generate_answer(question, context)