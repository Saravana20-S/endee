


from ingestion.clone_repo import clone_repository
from ingestion.extract_files import extract_code_files
from ingestion.chunk_code import chunk_code
from embeddings.embedding_model import generate_embeddings
from vectordb.endee_client import store_embeddings_batch

def process_repository(repo_url):
    print("🚀 Starting repository processing...")

    repo_path = clone_repository(repo_url)
    files = extract_code_files(repo_path)
    print(f"✅ Files extracted: {len(files)}")

    all_chunks = []
    for file in files:
        file_path = file.get("path", "unknown")
        code = file.get("content", "")
        if not code.strip():
            continue
        chunks = chunk_code(code)
        for chunk in chunks:
            all_chunks.append({"file": file_path, "code": chunk})

    if not all_chunks:
        return {"files": len(files), "chunks": 0, "embeddings": 0}

    texts = [c["code"] for c in all_chunks]
    embeddings = generate_embeddings(texts)
    metadatas = [{"file": c["file"], "code": c["code"]} for c in all_chunks]
    store_embeddings_batch(embeddings, metadatas)

    return {
        "files": len(files),
        "chunks": len(all_chunks),
        "embeddings": len(all_chunks)
    }