import streamlit as st
from embedder import Retriever
from util import on_similarity_change, on_citation_change, on_court_stats_change, pdf_to_text, close_all
from evaluator import evaluate_case

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

include_citation = st.sidebar.checkbox("Include Citation")

st.sidebar.subheader("Document Retrieval Count")
num_docs_input = st.sidebar.text_input("Enter number of documents to retrieve", value="10")

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

uploaded_file = st.file_uploader('Choose your .pdf file',type="pdf", accept_multiple_files = False)
if uploaded_file is not None:
    query_text = pdf_to_text(uploaded_file)

# Run button to trigger the retrieval process
if st.button("Run"):
    
    # Retrieve similar cases using the provided query
    df = retriever.search_similar_cases(query_text, similarity_weight=st.session_state.similarity, court_weight= st.session_state.court_stats, case_weight= st.session_state.citation,top_k=num_docs)

    # Store results in session state so they persist across reruns.
    st.session_state["results_df"] = df

    # Initialize a toggle state for each document to control the expander display.
    for row in df.iter_rows(named = True):
        case_name = row["Case"]
        st.session_state[f"show_summary_{case_name}"] = False
        st.session_state[f"show_eval_{case_name}"] = False

# If we have retrieval results stored, display them.
if "results_df" in st.session_state:

    df = st.session_state["results_df"]

    st.write("Retrieved Documents:")

    # For each retrieved document, create a vertical button.
    for row in df.iter_rows(named = True):

        case, summary, evaluation  = st.columns([2,1,1])

        case_name = row["Case"]

        with case:
            st.write(case_name)

        # For the Summary section:
        with summary:
            if st.button("LLM Summary", key=f"button_{case_name}"):
                # If the summary for this case is not already open, close all others.
                if not st.session_state.get(f"show_summary_{case_name}", False):
                    close_all()
                # Toggle the current summary state.
                st.session_state[f"show_summary_{case_name}"] = not st.session_state.get(f"show_summary_{case_name}", False)

        if st.session_state.get(f"show_summary_{case_name}", False):
            with st.expander(f"LLM Summary of {case_name}", expanded=True):
                st.write(row["CourtName"])
                st.write(row["Summary"])

        # For the Evaluation section:
        with evaluation:
            if st.button(f"LLM Evaluation", key=f"eval_{case_name}"):
                # If the evaluation for this case is not already open, close all others.
                if not st.session_state.get(f"show_eval_{case_name}", False):
                    close_all()
                # Toggle the current evaluation state.
                st.session_state[f"show_eval_{case_name}"] = not st.session_state.get(f"show_eval_{case_name}", False)

        if st.session_state.get(f"show_eval_{case_name}", False):
            with st.expander(f"LLM Evaluation of Current Dispute", expanded=True):
                st.write(evaluate_case(row["Summary"], query_text))
