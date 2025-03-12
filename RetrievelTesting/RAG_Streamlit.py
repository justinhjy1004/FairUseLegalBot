import streamlit as st
import polars as pl
from util import Retriever

## Initialize Retriever

retriever = Retriever()

# ---------------------------
# Sidebar Options
# ---------------------------

st.sidebar.title("Options")

st.sidebar.subheader("RAG Method Components")
#use_gemini = st.sidebar.checkbox("Use Gemini?", value=False)
use_similarity = st.sidebar.checkbox("Use Similarity", value=True)
use_citation = st.sidebar.checkbox("Use Citation")
use_court_stats = st.sidebar.checkbox("Use Court Stats")
use_graph_stats = st.sidebar.checkbox("Use Graph Stats (PageRank)")
#select_all = st.sidebar.checkbox("ALL DOCUMENTS")

st.sidebar.subheader("Document Retrieval Count")
num_docs_input = st.sidebar.text_input("Enter number of documents to retrieve", value="5")

# Validate numeric input; if invalid, default to 1.
try:
    num_docs = int(num_docs_input)
    if num_docs < 1:
        st.sidebar.error("Please enter a number greater than or equal to 1.")
        num_docs = 1
except ValueError:
    st.sidebar.error("Please enter a valid number.")
    num_docs = 1

# ---------------------------
# Main Page
# ---------------------------
st.title("Retrieval Testing Application")

# Input text area (query describing a case)
query_text = st.text_area("Enter your case description", height=150)

# Run button to trigger the retrieval process
if st.button("Run"):

    df = retriever.search_similar_cases(query_text, top_k=num_docs)
        
    # Display the retrieved document titles in a table.
    st.write("Retrieved Documents:")
    st.table(df)
