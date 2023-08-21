import json
import vector_db
import compiler


def test_code():
    # docs = compiler.parse_code("./temp_code/quote_disp")
    # for doc in docs:
    #     vector_db.index_document(doc)
    prompt_code_assistant("what framework is used in this code base ?")


def prompt_code_assistant(query):
    embed_query = vector_db.embed_text(query)
    results = vector_db.search(embed_query)
    matches = results["matches"]
    result = [match["metadata"]["meta"] for match in matches]
    results = vector_db.answer_question(query,  result)
    return results


test_code()
