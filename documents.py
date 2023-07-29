# documents.py

class FunctionDoc:
    def __init__(self, name, docstrings):
        self.name = name
        self.docstrings = docstrings


class ClassDoc:
    def __init__(self, name, docstrings):
        self.name = name
        self.docstrings = docstrings


class Document:
    def __init__(self, filepath, file_name, docstrings, functions, classes):
        self.filepath = filepath
        self.file_name = file_name
        self.docstrings = docstrings
        self.functions = functions
        self.classes = classes