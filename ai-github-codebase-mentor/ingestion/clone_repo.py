


# ingestion/clone_repo.py
import os
import git
from config.settings import settings

def clone_repository(repo_url: str):
    """Clones a GitHub repo to the local data directory."""
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    target_path = os.path.join(settings.REPO_STORAGE_PATH, repo_name)
    
    if os.path.exists(target_path):
        print(f"Repo {repo_name} already exists at {target_path}. Skipping clone.")
        return target_path

    print(f"Cloning {repo_url} into {target_path}...")
    git.Repo.clone_from(repo_url, target_path)
    return target_path


if __name__ == "__main__":
    test_url = "https://github.com/psf/requests" 
    path = clone_repository(test_url)
    print(f"Verification: Files cloned to {path}")