import os
import subprocess


def find_python_files(root_path):
    python_files = []
    for root, _, files in os.walk(root_path):
        for file_name in files:
            if file_name.endswith(".py"):
                full_path = os.path.join(root, file_name)
                python_files.append(full_path)
    return python_files


def run_quality_tools(python_files):
    for file in python_files:
        print(f"\nRunning checks on: {file}")
        subprocess.run(["black", file])
        subprocess.run(["flake8", file])


if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    files = find_python_files(root)

    if files:
        run_quality_tools(files)
    else:
        print("No Python files found.")

# pip install black
# pip install flake8
