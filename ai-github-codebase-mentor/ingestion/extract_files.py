



# ingestion/extract_files.py
import os

# Define extensions we want to index (feel free to add more)
ALLOWED_EXTENSIONS = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.md'}

def get_code_files(repo_path):
    """Walks through the repo and collects paths of source code files."""
    code_contents = []
    
    for root, dirs, files in os.walk(repo_path):
        # Skip hidden directories like .git
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if content.strip(): 
                            code_contents.append({
                                "file_path": os.path.relpath(file_path, repo_path),
                                "content": content
                            })
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")
                    
    return code_contents