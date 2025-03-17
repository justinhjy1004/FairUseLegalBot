import streamlit as st
from embedder import Retriever
from util import on_similarity_change, on_citation_change, on_court_stats_change

## Initialize Retriever

retriever = Retriever()

# ---------------------------
# Sidebar Options
# ---------------------------

st.sidebar.title("Options")

st.sidebar.subheader("RAG Method Components")

# ---------------------------
# Initialize weights in session state
# ---------------------------
if "similarity" not in st.session_state:
    st.session_state.similarity = 0.33
if "citation" not in st.session_state:
    st.session_state.citation = 0.33
if "court_stats" not in st.session_state:
    st.session_state.court_stats = 0.34

st.sidebar.slider(
    "Textual Similarity Weight",
    min_value=0.0,
    max_value=1.0,
    value=st.session_state.similarity,
    key="similarity",
    on_change=on_similarity_change,
)
st.sidebar.slider(
    "Citation Weight",
    min_value=0.0,
    max_value=1.0,
    value=st.session_state.citation,
    key="citation",
    on_change=on_citation_change,
)
st.sidebar.slider(
    "Court Weight",
    min_value=0.0,
    max_value=1.0,
    value=st.session_state.court_stats,
    key="court_stats",
    on_change=on_court_stats_change,
)

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
    # Retrieve similar cases using the provided query
    df = retriever.search_similar_cases(query_text, top_k=num_docs)
    # Store results in session state so they persist across reruns.
    st.session_state["results_df"] = df

    # Initialize a toggle state for each document to control the expander display.
    for i in df.index:
        st.session_state[f"show_summary_{i}"] = False

# If we have retrieval results stored, display them.
if "results_df" in st.session_state:
    
    df = st.session_state["results_df"]
    st.write("Retrieved Documents:")

    # For each retrieved document, create a vertical button.
    for i, row in df.iterrows():

        case_name = row["Case"]

        # When the button is clicked, toggle the corresponding summary display flag.
        if st.button(case_name, key=f"button_{i}"):
            st.session_state[f"show_summary_{i}"] = not st.session_state.get(f"show_summary_{i}", False)

        # If the flag is True, display an expander with the summary.
        if st.session_state.get(f"show_summary_{i}", False):
            with st.expander(f"Summary for {case_name}", expanded=True):
                st.write(row["Summary"])
