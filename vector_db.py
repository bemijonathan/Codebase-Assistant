# vector_db.py

import time
import numpy as np
import pinecone
from sentence_transformers import SentenceTransformer
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# Connect to Pinecone
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"),
              environment=os.getenv("PINECONE_ENV"))

index_name = 'tests'

# Embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')


def sleep():
    time.sleep(15)


def embed_text(text):
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response["data"][0]["embedding"]


def index_document(doc):
    index = pinecone.Index(index_name=index_name)
    d = doc.docstrings
    vector = embed_text(d)

    index.upsert([(doc.file_name, vector, {"meta": d})])
    sleep()


def search(query_vector):
    index = pinecone.Index(index_name=index_name)
    return index.query([query_vector], top_k=5, include_metadata=True)


def answer_question(question, texts):
    prompt = 'using the ast from this codebase answer this question: question: ' + \
        question + ' AST: '.join(texts)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system",
                "content": "Assistant is a large language model trained by OpenAI."},
            {"role": "user", "content": f"Question: {prompt}"},
        ],
        max_tokens=500
    )

    return response['choices'][0]['message']['content']
