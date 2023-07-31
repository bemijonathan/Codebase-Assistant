from typing import Optional, List


class FunctionDoc:

    def __init__(self,
                 name: str,
                 params: List[str],
                 docstring: Optional[str] = '',
                 decorators: List[str] = None,
                 location: tuple = None):

        self.name = name
        self.params = params
        self.docstring = docstring
        self.decorators = decorators if decorators else []
        self.location = location


class ClassDoc:
    def __init__(self, name, docstrings):
        self.name = name
        self.docstrings = docstrings


class Document:

    def __init__(self, filepath: str, file_name: str, docstrings: str,
                 functions: list[FunctionDoc], classes: list[ClassDoc],
                 tokens: list[int]) -> None:

        self.filepath = filepath
        self.file_name = file_name
        self.docstrings = docstrings
        self.functions = functions
        self.classes = classes
        self.tokens = tokens
