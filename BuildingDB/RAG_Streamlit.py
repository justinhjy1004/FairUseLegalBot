import streamlit as st
import pandas as pd

# ---------------------------
# Mock Data
# ---------------------------
# Simulated database: a list of document titles.
mock_data = [
    {"title": "Document 1: Case Analysis on X"},
    {"title": "Document 2: Research on Y"},
    {"title": "Document 3: Overview of Z"},
    {"title": "Document 4: Deep Dive on A"},
    {"title": "Document 5: Study of B"},
    {"title": "Document 6: Report on C"},
    {"title": "Document 7: Summary of D"},
    {"title": "Document 8: Findings on E"},
    {"title": "Document 9: Insights on F"},
    {"title": "Document 10: Examination of G"},
    {"title": "Document 11: Evaluation of H"},
    {"title": "Document 12: Analysis on I"},
    {"title": "Document 13: Case Review on J"},
    {"title": "Document 14: Survey on K"},
    {"title": "Document 15: Discussion on L"},
    {"title": "Document 16: Study on M"},
    {"title": "Document 17: Overview of N"},
    {"title": "Document 18: Report on O"},
    {"title": "Document 19: Investigation on P"},
    {"title": "Document 20: Analysis on Q"},
    # Extend to <300 documents as needed.
]

# ---------------------------
# Sidebar Options
# ---------------------------
st.sidebar.title("Options")

st.sidebar.subheader("RAG Method Components")
use_similarity = st.sidebar.checkbox("Use Similarity", value=True)
use_reranking = st.sidebar.checkbox("Use Reranking")
use_nearest_neighbors = st.sidebar.checkbox("Use Nearest-Neighbors")
use_graph_stats = st.sidebar.checkbox("Use Graph Stats (PageRank)")
select_all = st.sidebar.checkbox("ALL DOCUMENTS")

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
st.title("RAG Testing Application")

# Input text area (query describing a case)
query_text = st.text_area("Enter your case description", height=150)

# Run button to trigger the retrieval process
if st.button("Run"):

    # Determine documents to retrieve: if ALL DOCUMENTS is checked, ignore num_docs.
    if select_all:
        result_docs = mock_data
    else:
        result_docs = mock_data[:num_docs]
    
    # Display the retrieved document titles in a table.
    df = pd.DataFrame(result_docs)
    st.write("Retrieved Documents:")
    st.table(df)
