import ast
import os
import extraction
from documents import FunctionDoc, ClassDoc, Document
from typing import List


def get_all_py_files(code_dir: str) -> List({
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
                    'content': content
                })
    return py_files


def process_functions(func_nodes: list[ast.FunctionDef]):
    functions = []
    for func_node in func_nodes:
        func_doc = FunctionDoc(
            name=func_node.name,
            params=[p.arg for p in func_node.args.args],
            docstring=ast.get_docstring(func_node),
            decorators=[d.name for d in func_node.decorator_list]
        )
        functions.append(func_doc)

    return functions


def process_classes(class_nodes: List[ast.ClassDef]):
    classes = []
    for class_node in class_nodes:
        class_doc = ClassDoc(
            name=class_node.name,
            methods=[n.name for n in class_node.body if isinstance(
                n, ast.FunctionDef)],
            docstring=ast.get_docstring(class_node)
        )
        classes.append(class_doc)

    return classes


def parse_code(code_dir: str) -> List[str]:
    docs = []
    for filepath in get_all_py_files(code_dir):
        metadata = extraction.extract_metadata(filepath)
        function_docs = process_functions(metadata["functions"])
        class_docs = process_classes(metadata["classes"])

        doc = Document(
            filepath=filepath['path'],
            docstrings=filepath["content"],
            function_docs=function_docs,
            class_docs=class_docs,
            tokens=metadata["tokens"]
        )

        docs.append(doc)

    return docs


# TODO: remove for testing
# parse_code("./temp_code/quote_disp")
