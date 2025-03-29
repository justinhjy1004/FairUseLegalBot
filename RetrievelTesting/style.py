import streamlit as st

def apply_custom_file_uploader_style():
    custom_css = """
        <style>
        .stFileUploader {
            display: none;
        }
        .custom-upload-btn {
            display: inline-block;
            padding: 0.5rem 1rem;
            background-color: #4CAF50;
            color: white;
            font-size: 1rem;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            text-align: center;
        }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def custom_file_uploader(label="Upload PDF File"):
    st.markdown(f'<label class="custom-upload-btn">{label}</label>', unsafe_allow_html=True)
    return st.file_uploader(label=label, label_visibility="collapsed", type="pdf", accept_multiple_files = False)
