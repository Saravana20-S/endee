# test_ingestion.py
from ingestion.clone_repo import clone_repository
from ingestion.extract_files import get_code_files
from ingestion.chunk_code import process_repo_into_chunks

# 1. Clone
repo_url = "https://github.com/psf/requests" 
path = clone_repository(repo_url)

# 2. Extract
files = get_code_files(path)
print(f"✅ Extracted {len(files)} files.")

# 3. Chunk
chunks = process_repo_into_chunks(files)
print(f"✅ Generated {len(chunks)} chunks.")

if chunks:
    print(f"Sample Chunk from {chunks[0]['metadata']['file_path']}:")
    print(chunks[0]['text'][:200] + "...")