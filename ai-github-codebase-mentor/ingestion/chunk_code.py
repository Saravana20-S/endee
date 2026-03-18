

# ingestion/chunk_code.py
from config.settings import settings

def chunk_text(text, chunk_size=settings.CHUNK_SIZE, overlap=settings.CHUNK_OVERLAP):
    """Simple sliding window chunking."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks

def process_repo_into_chunks(code_files):
    """Processes list of files into metadata-rich chunks."""
    all_chunks = []
    
    for file_data in code_files:
        chunks = chunk_text(file_data['content'])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk,
                "metadata": {
                    "file_path": file_data['file_path'],
                    "chunk_id": i
                }
            })
    return all_chunks