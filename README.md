# Code Assistant 

Code Assistant is an AI-powered code comprehension assistant. It allows users to upload a codebase and ask natural language questions to understand the code.

## Features

- Upload a codebase (currently supports Python)
- Advanced static analysis of the code using AST parsing 
- Extraction of key metadata - functions, classes, call graphs, etc.
- Vectorization and indexing of code snippets and documentation
- Natural language conversational interface using Streamlit
- Powered by transformer models like Codex and LangChain for code intelligence

## How it Works

1. User uploads a Python codebase via Streamlit UI

2. Code is parsed using AST module to extract metadata

3. HuggingFace tokenizers used to generate code embeddings 

4. Metadata and tokens indexed into vector database

5. User asks code comprehension questions in NL

6. LangChain model answers questions by searching database

7. Codex used for suggestions on edits, fixes, etc.

## Getting Started

```
# Install dependencies
pip install -r requirements.txt

# Run Streamlit UI
streamlit run app.py
```

## Next Steps

- Support more languages like JavaScript, Java
- Add integration tests
- Improve parser for more robust metadata  
- Enhance LangChain model with more training
- Add user workflow for followup questions

## Contributing

Contributions to improve the project are welcome! Please open issues and pull requests.

Let me know if you would like me to expand or modify any part of this high-level README!