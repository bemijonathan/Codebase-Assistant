from typing import List


class FunctionDoc:
    def __init__(self, name, docstrings):
        self.name = name
        self.docstrings = docstrings


class ClassDoc:
    def __init__(self, name, docstrings):
        self.name = name
        self.docstrings = docstrings


class Document:

    def __init__(self, filepath: str, file_name: str, docstrings: str,
                 functions: List[FunctionDoc], classes: List[ClassDoc],
                 tokens: List[int]) -> None:

        self.filepath = filepath
        self.file_name = file_name
        self.docstrings = docstrings
        self.functions = functions
        self.classes = classes
        self.tokens = tokens
