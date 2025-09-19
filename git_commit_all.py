""" 
poetry run python git_commit_all.py 
"""


import subprocess
import sys
from datetime import datetime
from pathlib import Path

PYTHON_GITIGNORE = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs and editors
.vscode/
.idea/
*.sublime-project
*.sublime-workspace

# MyPy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# Profiling
.prof
"""

def ensure_git_repo(repo_path: Path):
    """Ensure the current folder is a git repo, init if not."""
    git_dir = repo_path / ".git"
    if not git_dir.exists():
        print("No .git folder found, initializing a new Git repository...")
        try:
            subprocess.run(["git", "init"], cwd=repo_path, check=True)
            print("Initialized empty Git repository.")

            # Create a .gitignore for Python projects
            gitignore_file = repo_path / ".gitignore"
            if not gitignore_file.exists():
                gitignore_file.write_text(PYTHON_GITIGNORE, encoding="utf-8")
                print("Created .gitignore for Python.")

            # Make the first commit
            subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=repo_path,
                check=True,
            )
            print("Created initial commit.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to initialize git repo: {e}")
            sys.exit(1)
    else:
        print("Git repository already exists.")


def git_commit_all():
    """
    Stage all changes, commit, and push to the current Git repository.
    Asks the user for a commit title and description.
    """
    repo_path = Path.cwd()
    ensure_git_repo(repo_path)

    # Ask for commit title
    commit_title = input("Enter commit title (short): ").strip()
    if not commit_title:
        commit_title = f"Auto-commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # Ask for optional description
    commit_description = input("Enter commit description (optional): ").strip()
    if commit_description:
        commit_message = f"{commit_title}\n\n{commit_description}"
    else:
        commit_message = commit_title

    try:
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        print("Staged all changes.")

        subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
        print(f"Committed changes with message:\n{commit_message}")

        subprocess.run(["git", "push"], cwd=repo_path, check=True)
        print("Pushed changes to remote repository.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    git_commit_all()