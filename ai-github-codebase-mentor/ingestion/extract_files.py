# import os
# from config.settings import SUPPORTED_EXTENSIONS

# def extract_code_files(repo_path):

#     code_files = []

#     for root, dirs, files in os.walk(repo_path):

#         for file in files:

#             if any(file.endswith(ext) for ext in SUPPORTED_EXTENSIONS):

#                 code_files.append(os.path.join(root, file))

#     return code_files


import os

SUPPORTED_EXTENSIONS = [".py", ".js", ".java", ".html", ".css"]

def extract_code_files(repo_path):

    files = []

    for root, dirs, filenames in os.walk(repo_path):

        for filename in filenames:

            if any(filename.endswith(ext) for ext in SUPPORTED_EXTENSIONS):

                filepath = os.path.join(root, filename)

                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()

                    files.append({
                        "path": filepath,
                        "content": content
                    })

                except Exception:
                    pass

    print("Files extracted:", len(files))

    return files