# from ingestion.clone_repo import clone_repository
# from ingestion.extract_files import extract_code_files
# from ingestion.chunk_code import chunk_code
# from embeddings.embedding_model import generate_embeddings
# from vectordb.endee_client import store_embedding
# from utils.file_utils import read_file


# def process_repository(repo_url):

#     repo_path = clone_repository(repo_url)

#     files = extract_code_files(repo_path)

#     for file in files:

#         code = read_file(file)

#         chunks = chunk_code(code)

#         for chunk in chunks:

#             embedding = generate_embedding(chunk)

#             store_embedding(
#                 embedding,
#                 {
#                     "file": file,
#                     "code": chunk
#                 }
#             )



from ingestion.clone_repo import clone_repository
from ingestion.extract_files import extract_code_files
from ingestion.chunk_code import chunk_code
from embeddings.embedding_model import generate_embeddings
from vectordb.endee_client import store_embedding
from utils.file_utils import read_file


def process_repository(repo_url):

    print("Cloning repository...")
    repo_path = clone_repository(repo_url)

    print("Extracting code files...")
    files = extract_code_files(repo_path)

    all_chunks = []

    for file in files:

        try:
            code = read_file(file)

            chunks = chunk_code(code)

            for chunk in chunks:
                all_chunks.append({
                    "file": file,
                    "code": chunk
                })

        except Exception as e:
            print("Error reading file:", file, e)

    print("Total chunks:", len(all_chunks))

    # Prepare text list for embeddings
    texts = [c["code"] for c in all_chunks]

    print("Generating embeddings...")
    embeddings = generate_embeddings(texts)

    print("Storing embeddings in vector DB...")

    for chunk_data, embedding in zip(all_chunks, embeddings):

        store_embedding(
            embedding,
            {
                "file": chunk_data["file"],
                "code": chunk_data["code"]
            }
        )

    print("Repository processing complete")

    return {
        "files": len(files),
        "chunks": len(all_chunks),
        "embeddings": len(embeddings)
    }