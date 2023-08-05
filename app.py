import streamlit as st
import os
from zipfile import ZipFile
import shutil
import compiler
import vector_db


def prompt_code_assistant(query):
    embed_query = vector_db.embed_text(query)
    results = vector_db.search(embed_query)
    matches = results["matches"]
    result = [match["metadata"]["meta"] for match in matches]
    results = vector_db.answer_question(query,  result)
    return results


st.title("Codebase Assistant")

question = st.text_input(
    "Ask a question about the code base"
)

button = st.form_submit_button("Submit")


if question:
    d = prompt_code_assistant(question)
    print(d)
    st.text(d)

# Add side bar for adding questions
with st.sidebar:
    # Allow uploading zipped code folder
    uploaded_file = st.file_uploader(
        "Upload code folder (zipped, < 1MB)", type=['zip'])

if uploaded_file is not None:

    # Save uploaded file to temp dir
    bytes_data = uploaded_file.getvalue()
    temp_dir = os.path.join("temp_code")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    else:
        shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

    with open(os.path.join(temp_dir, "code.zip"), "wb") as f:
        f.write(bytes_data)

    # Size check
    if os.path.getsize(os.path.join(temp_dir, "code.zip")) > 1e6:
        st.error("Code folder too large. Please upload a zip less than 1MB.")
    else:
        # Unzip
        with ZipFile(os.path.join(temp_dir, "code.zip"), 'r') as zipObj:
            zipObj.extractall(temp_dir)

        docs = compiler.parse_code("./temp_code/quote_disp")
        for doc in docs:
            vector_db.index_document(doc)

        st.success("Code folder uploaded!")
