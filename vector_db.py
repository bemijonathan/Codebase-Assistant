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

    # Embed functions
    for func in doc.functions:
        sleep()  # Rate limit OpenAI calls
        text = func.name + (func.docstring or "")
        vector = embed_text(text)
        index.upsert(vectors=[(func.name, vector)])

    # Embed classes
    for cls in doc.classes:
        sleep()  # Rate limit OpenAI calls
        text = cls.name + (cls.docstring or "")
        vector = embed_text(text)
        index.upsert(vector=[(cls.name,  vector)])

    # Index tokens
    sleep()  # Rate limit OpenAI calls
    token_vectors = embed_text(doc.tokens)

    index.upsert(vectors=[('tokens', token_vectors)])


def search(query_vector):
    index = pinecone.Index(index_name=index_name)

    return index.query([query_vector], top_k=5)


def answer_question(texts):
    # Combine the texts into a single string
    prompt = ' '.join(texts)

    # Generate a follow-up response using OpenAI's API
    response = openai.Completion.create(
        # TODO: should be using davincis model or codex
        engine="text-similarity-davinci-001",
        prompt=prompt,
        max_tokens=100
    )

    # Return the generated text
    return response['choices'][0]['text']['content']
