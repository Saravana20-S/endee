import os
from git import Repo
from config.settings import REPO_STORAGE_PATH

def clone_repository(repo_url):

    if not os.path.exists(REPO_STORAGE_PATH):
        os.makedirs(REPO_STORAGE_PATH)

    repo_name = repo_url.split("/")[-1]
    repo_path = os.path.join(REPO_STORAGE_PATH, repo_name)

    if os.path.exists(repo_path):
        return repo_path

    Repo.clone_from(repo_url, repo_path)

    return repo_path 