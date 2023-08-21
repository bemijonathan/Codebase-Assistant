from time import sleep
import streamlit as st
import os
from zipfile import ZipFile
import shutil
import compiler
import vector_db

def prompt_code_assistant(query, namespace):
    embed_query = vector_db.embed_text(query)
    results = vector_db.search(embed_query, namespace)
    matches = results["matches"]
    result = [match["metadata"]["meta"] for match in matches]
    results = vector_db.answer_question(query,  result)
    return results


st.title("Codebase Assistant")



def main():
    st.sidebar.title("Select Previously Uploaded codebase")
    st.sidebar.write("Select a previously uploaded codebase to query")
    st.sidebar.selectbox("Select a previously uploaded codebase to query", vector_db.get_namespaces())
        
    
        # Allow uploading zipped code folder
    uploaded_file = st.file_uploader(
        "Upload code folder (zipped, < 1MB)", type=['zip'])

    with st.form("my_form"):
        st.write("Inside the form")
        question = st.text_input(
            "Ask a question about the code base"
        )
        # TODO:
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            os.path.basename(os.path.dirname(uploaded_file.name))
            d = prompt_code_assistant(question,uploaded_file.name[:-4])
            st.write(d)
            return

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
            docs_space = uploaded_file.name[:-4]
            docs = compiler.parse_code(f"./temp_code/{docs_space}")
            st.warning("Crunching codebase... please wait a few minutes.")
            for doc in docs:
                sleep(20)
                vector_db.index_document(doc, docs_space)

            st.success("Code folder uploaded!")

main()