import os
import shutil

class RepoUtils:
    @staticmethod
    def get_repo_size(path: str) -> int:
        """Get repository size in MB."""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size // (1024 * 1024)
