import os
import subprocess


WORKSPACE = "workspace"


def list_files():

    files = []

    for root, dirs, filenames in os.walk(WORKSPACE):

        for filename in filenames:

            path = os.path.join(root, filename)

            files.append(path)

    return files


def read_file(path: str):

    full_path = os.path.join(WORKSPACE, path)

    if not os.path.exists(full_path):
        return f"File not found: {path}"

    with open(full_path, "r", encoding="utf-8") as file:
        return file.read()


def write_file(path: str, content: str):

    full_path = os.path.join(WORKSPACE, path)

    directory = os.path.dirname(full_path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as file:
        file.write(content)

    return f"Successfully wrote {path}"


def run_tests():

    try:

        result = subprocess.run(
            ["pytest", WORKSPACE],
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:

        return {
            "return_code": -1,
            "stdout": "",
            "stderr": "Tests timed out"
        }