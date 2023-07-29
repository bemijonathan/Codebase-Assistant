import streamlit as st
import os
from zipfile import ZipFile

st.title("Codebase Assistant")

# Allow uploading zipped code folder
uploaded_file = st.file_uploader("Upload code folder (zipped, < 1MB)", type=['zip'])

# Add side bar for adding questions
with st.sidebar:
    add_input = st.text_input(
        "Ask a question about the code base"
    )


if uploaded_file is not None:

    # Save uploaded file to temp dir
    bytes_data = uploaded_file.getvalue()
    temp_dir = os.path.join("temp_code")
    if not os.path.exists(temp_dir):
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

        st.success("Code folder uploaded!")