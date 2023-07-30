from transformers import AutoTokenizer
from ast import parse
import re

TOKENIZERS = {
    "python": 'distilgpt2',
    "js": 'js'
}


def tokenize_code(code, language):
    # TODO: remove and make the tokenizer a dynamic variable based on the file type
    tokenizer = AutoTokenizer.from_pretrained('distilgpt2')

    # Preprocess code
    code = preprocess(code)

    # Tokenize
    tokens = tokenizer.encode(code)

    return tokens


def preprocess(code):
    # Remove backticks
    code = re.sub("`+", "", code)

    # Remove Python docstrings
    code = re.sub('""".+"""', "", code)

    return code


def get_language(file_path: str) -> str:
    if file_path.endswith('.py'):
        return TOKENIZERS['python']
    elif file_path.endswith('.js'):
        return TOKENIZERS['js']
    else:
        SystemError("Language not supported")


def extract_metadata(file_path: {
    'path': str,
    'content': str
}):

    # Parse AST
    ast = parse(file_path['content'])

    # Extract AST metadata
    functions = []
    for node in ast.body:
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

    classes = []
    for node in ast.body:
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)

    # Tokenize code
    language = get_language(file_path['path'])
    tokens = tokenize_code(file_path['content'], language)

    return {
        "ast": ast,
        "functions": functions,
        "classes": classes,
        "tokens": tokens
    }
