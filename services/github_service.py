import os
import shutil
import tempfile
import uuid
from git import Repo
from typing import Tuple

class GitHubService:
    @staticmethod
    def clone_repository(repo_url: str) -> Tuple[str, str]:
        """Clone a public GitHub repository to a temporary directory."""
        temp_dir = os.path.join(tempfile.gettempdir(), f"devflow_{uuid.uuid4().hex}")
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            Repo.clone_from(repo_url, temp_dir)
            repo_name = repo_url.rstrip("/").split("/")[-1]
            return temp_dir, repo_name
        except Exception as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise Exception(f"Failed to clone repository: {str(e)}")

    @staticmethod
    def cleanup(path: str):
        """Remove the cloned repository directory."""
        shutil.rmtree(path, ignore_errors=True)
