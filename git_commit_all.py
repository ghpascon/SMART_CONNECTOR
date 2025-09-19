"""
poetry run python git_commit_all.py
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_git_command(args, repo_path, check=True, capture_output=False):
    return subprocess.run(
        ["git"] + args,
        cwd=repo_path,
        check=check,
        capture_output=capture_output,
        text=True,
    )


def git_commit_all():
    """
    Stage all changes, commit, and push to the current Git repository.
    Initializes repo if it doesn't exist.
    """
    repo_path = Path.cwd()

    # Check if .git exists
    if not (repo_path / ".git").exists():
        print("No Git repository found. Initializing...")
        run_git_command(["init"], repo_path)

        # Create .gitignore for Python
        gitignore = repo_path / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text(
                """# Byte-compiled / cache
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
.venv/
env/
venv/
ENV/

# Distribution / packaging
build/
dist/
*.egg-info/

# IDEs
.vscode/
.idea/
"""
            )
            print("Created .gitignore for Python.")

        run_git_command(["add", "."], repo_path)
        run_git_command(
            ["commit", "-m", "Initial commit"], repo_path, check=False
        )
        print("Created initial commit.")

    # Ask for commit title
    commit_title = input("Enter commit title (short): ").strip()
    if not commit_title:
        commit_title = f"Auto-commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # Ask for optional description
    commit_description = input("Enter commit description (optional): ").strip()
    commit_message = f"{commit_title}\n\n{commit_description}" if commit_description else commit_title

    try:
        # Stage changes
        run_git_command(["add", "."], repo_path)
        print("Staged all changes.")

        # Check if there is anything to commit
        status = run_git_command(
            ["status", "--porcelain"], repo_path, capture_output=True
        )
        if not status.stdout.strip():
            print("Nothing to commit. Working tree clean.")
            return

        # Commit
        run_git_command(["commit", "-m", commit_message], repo_path)
        print(f"Committed changes with message:\n{commit_message}")

        # Push
        try:
            run_git_command(["push"], repo_path)
            print("Pushed changes to remote repository.")
        except subprocess.CalledProcessError:
            print("Push failed. Maybe no remote set? Run:\n  git remote add origin <url>")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    git_commit_all()
