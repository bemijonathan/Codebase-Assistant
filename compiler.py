import ast
import os

from documents import FunctionDoc, ClassDoc, Document

import os


def get_all_py_files(code_dir):
    py_files = []

    for root, dirs, files in os.walk(code_dir):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))

    return py_files


def parse_code(code_dir):
    docs = []

    for filepath in get_all_py_files(code_dir):
        tree = ast.parse(open(filepath))
        file_name = os.path.basename(filepath)
        file_docstrings = ast.get_docstring(tree)

        functions = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                func_doc = get_function_docs(node)
                functions.append(func_doc)

        classes = []
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                class_doc = get_class_docs(node)
                classes.append(class_doc)

        doc = Document(filepath,
                       file_name=file_name,
                       docstrings=file_docstrings,
                       functions=functions,
                       classes=classes)
        docs.append(doc)

    return docs


def get_function_docs(func_node):
    func_name = func_node.name
    func_docstrings = ast.get_docstring(func_node)

    return FunctionDoc(name=func_name, docstrings=func_docstrings)


def get_class_docs(class_node):
    class_name = class_node.name
    class_docstrings = ast.get_docstring(class_node)

    return ClassDoc(name=class_name, docstrings=class_docstrings)