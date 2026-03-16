from config.settings import CHUNK_SIZE

# def chunk_code(code):

#     chunks = []

#     for i in range(0, len(code), CHUNK_SIZE):

#         chunks.append(code[i:i + CHUNK_SIZE])

#     return chunks



def chunk_code(code, chunk_size=500):

    chunks = []

    if not code:
        return chunks

    code = str(code)

    for i in range(0, len(code), chunk_size):

        chunk = code[i:i + chunk_size]

        if chunk.strip():  # ignore empty chunks
            chunks.append(chunk)

    print("Chunks created:", len(chunks))

    return chunks