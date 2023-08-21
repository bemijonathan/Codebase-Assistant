# vector_db.py

import time
import numpy as np
import pinecone
from sentence_transformers import SentenceTransformer
import os
import openai

from dotenv import load_dotenv

load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("ENVIRONMENT")
openai_api_key = os.getenv("OPENAI_API_KEY")

pinecone.init(api_key=pinecone_api_key, environment=environment)
index_name = 'code-assistant'
embedder = SentenceTransformer('all-MiniLM-L6-v2')


def sleep():
    time.sleep(1)


def embed_text(text):
    openai.api_key = openai_api_key
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response["data"][0]["embedding"]


def index_document(doc, namespace):
    with open('namespaces.txt', 'w') as f:
        f.write(namespace + '\n')
    index = pinecone.Index(index_name=index_name)
    d = doc.docstrings
    vector = embed_text(d)
    index.upsert(
        vectors=[(doc.file_name, vector, {"meta": d})], namespace=namespace)
    sleep()


def search(query_vector, namespace):
    index = pinecone.Index(index_name=index_name)
    return index.query([query_vector], top_k=5, include_metadata=True, namespace=namespace)

def get_namespaces():

  namespaces = []

  if os.path.exists('namespaces.txt'): 
    with open('namespaces.txt', 'r') as f:
      for line in f:
        namespace = line.strip()  
        namespaces.append(namespace)

  return namespaces
    


def answer_question(question, texts):
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {
                "role": "system", 
                "content": "Hello, I am a code assistant.I will only answer questions about the context below"
            },
            {
                "role": "user",
                "content": "Context: ____  "  + texts[0]
            }, 
            {
                "role": "system",
                "content": "sure i will help answer only questions about the context above" 
            }, 
            {
                "role": "user",
                "content": question
            }
        ],
        max_tokens=500
    )

    return response['choices'][0]['message']['content']
