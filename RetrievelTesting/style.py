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

def custom_file_uploader(label="Upload PDF File", key="file-upload"):
    st.markdown(f'<label for="{key}" class="custom-upload-btn">{label}</label>', unsafe_allow_html=True)
    return st.file_uploader(label, key=key, label_visibility="collapsed", type="pdf", custom_file_uploader = False)
