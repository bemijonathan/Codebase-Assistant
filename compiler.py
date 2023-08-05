import ast
import os
from documents import FunctionDoc, ClassDoc, Document


def get_all_py_files(code_dir: str) -> list({
    'path': str,
    'content': str
}):  # return a list of dictionaries
    py_files = []
    for root, dirs, files in os.walk(code_dir):
        for file in files:
            if file.endswith('.py') or file.endswith('.js'):
                file_path = os.path.join(root, file)
                with open(file_path) as f:
                    content = f.read()

                py_files.append({
                    'path': file_path,
                    'content': content,
                    'name': file
                })
    return py_files


def parse_code(code_dir: str) -> list[str]:
    docs = []
    for filepath in get_all_py_files(code_dir):
        doc = Document(
            filepath=filepath['path'],
            docstrings=filepath["content"],
            file_name=filepath['name']
        )

        docs.append(doc)

    return docs
