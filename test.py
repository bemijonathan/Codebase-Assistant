import vector_db
import compiler


def test_code():
    docs = compiler.parse_code("./temp_code/quote_disp")
    for doc in docs:
        vectoried_doc = vector_db.index_document(doc)
        print(vectoried_doc)


def prompt_code_assistant(query):
    embed_query = vector_db.embed_text(query)
    results = vector_db.search(embed_query)
    texts = [result['text'] for result in results]
    return texts


test_code()
