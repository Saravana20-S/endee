


import os
import json
import time
from config.settings import settings
from ingestion.clone_repo import clone_repository
from ingestion.extract_files import get_code_files
from ingestion.chunk_code import process_repo_into_chunks
from embeddings.embedding_model import embedder
from vectordb.endee_client import endee_client
from rag.generator import generator

class GitHubMentorPipeline:
    def __init__(self, index_name):
        # Normalize index name: force lowercase and underscores for Endee compatibility
        self.index_name = index_name.lower().replace(" ", "_")
        
        # Local "Source of Truth" path on E: drive
        self.storage_path = r"E:\endee\ai-github-codebase-mentor\data\embeddings"
        
        if not os.path.exists(self.storage_path):
            try:
                os.makedirs(self.storage_path)
            except Exception as e:
                print(f"⚠️ Warning: Could not create E: drive path. Error: {e}")

    def ingest_new_repo(self, repo_url):
        """Full pipeline: Clone -> Extract -> Chunk -> Embed -> Store."""
        print(f"--- 🚀 Starting Ingestion for {repo_url} ---")
        
        # 1. Pipeline Extraction
        repo_path = clone_repository(repo_url)
        files = get_code_files(repo_path)
        chunks_data = process_repo_into_chunks(files)
        
        if not chunks_data:
            print("❌ No code chunks extracted. Aborting.")
            return

        # 2. Reset/Create Endee Index
        print(f"🧹 Resetting index: {self.index_name}...")
        endee_client.delete_index(self.index_name)
        time.sleep(2) 
        endee_client.create_index(self.index_name)

        # 3. Processing, Embedding, and Syncing
        all_embeddings_log = []
        batch_size = 30
        total_inserted = 0

        for i in range(0, len(chunks_data), batch_size):
            batch = chunks_data[i:i+batch_size]
            batch_texts = [str(c['text']) for c in batch]
            
            # Metadata Sanitization: Crucial for Endee DB stability
            batch_metas = [
                {
                    "title": str(c['text'])[:1000], 
                    "file": str(c['metadata'].get('file', 'unknown')),
                    "chunk_id": str(i + j)
                } for j, c in enumerate(batch)
            ]
            
            vectors = embedder.generate_embeddings(batch_texts)
            
            # A. Sync to Endee DB
            endee_client.insert_vectors(self.index_name, vectors, batch_metas)

            # B. Prepare Local JSON Backup
            for j in range(len(batch)):
                all_embeddings_log.append({
                    "id": f"vec_{int(time.time())}_{i+j}",
                    "text": batch_texts[j],
                    "meta": batch_metas[j],
                    "vector": [float(v) for v in vectors[j]] 
                })

            total_inserted += len(batch)
            print(f"✅ Indexed Batch {i//batch_size + 1}")

        # 4. Save to E:\ drive
        json_file = os.path.join(self.storage_path, f"{self.index_name}_backup.json")
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(all_embeddings_log, f, indent=2)
            print(f"💾 Local Backup Saved: {json_file}")
        except Exception as e:
            print(f"❌ Failed to save JSON backup: {e}")
        
        print(f"🏁 Successfully indexed {total_inserted} chunks.")

    def ask_question(self, question):
        """Retrieval Augmented Generation loop with fallback logic."""
        # 1. Embed the question
        query_vector = embedder.generate_embeddings([question])[0]
        
        # 2. Retrieve from Endee (Passing query_vector first as per updated client)
        search_res = endee_client.search_vectors(query_vector, self.index_name, k=5)
        
        # 3. Parse the Results (The logic you liked)
        context = []
        
        # Check if we have a list (raw results) or a dict (wrapper)
        data = search_res if isinstance(search_res, list) else search_res.get('data', [])
        
        if isinstance(data, list):
            for item in data:
                # Based on our insert, content is in meta['title']
                # We check both 'meta' and 'metadata' just in case
                meta = item.get('meta') or item.get('metadata', {})
                content = meta.get('title', "")
                if content:
                    context.append(content)
        
        # 4. Fallback (This ensures the AI always answers)
        if not context:
            print("⚠️ DB returned no results. Using fallback context.")
            context = ["The database is currently empty or the specific code was not found. Please provide a general explanation of how this logic typically works in a Flask application."]
        
        # 5. Generate Answer via Gemini
        return generator.generate_answer(question, context)

    def delete_project(self):
        db_success = endee_client.delete_index(self.index_name)
        json_file = os.path.join(self.storage_path, f"{self.index_name}_backup.json")
        if os.path.exists(json_file):
            os.remove(json_file)
        return db_success