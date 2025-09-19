"""
    poetry run python git_commit_all.py
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

def git_commit_all(commit_message: str = None):
    """
    Stage all changes, commit, and push to the current Git repository.
    
    :param commit_message: Optional commit message. Defaults to timestamp.
    """
    repo_path = Path.cwd()  # Current directory
    if commit_message is None:
        commit_message = f"Auto-commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    try:
        # Stage all changes
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        print("Staged all changes.")

        # Commit changes
        subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
        print(f"Committed changes with message: '{commit_message}'")

        # Push to current branch
        subprocess.run(["git", "push"], cwd=repo_path, check=True)
        print("Pushed changes to remote repository.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    git_commit_all()
