import streamlit as st
import fitz

# ---------------------------
# Callback Functions
# ---------------------------
def on_similarity_change():
    # The new value set by the user:
    new_sim = st.session_state.similarity
    # Old values for the other two:
    old_citation = st.session_state.citation
    old_court = st.session_state.court_stats
    remaining = 1 - new_sim
    old_sum = old_citation + old_court
    if old_sum == 0:
        # Avoid division by zero; split equally.
        st.session_state.citation = remaining / 2
        st.session_state.court_stats = remaining / 2
    else:
        st.session_state.citation = old_citation / old_sum * remaining
        st.session_state.court_stats = old_court / old_sum * remaining

    st.cache_data.clear()

def on_citation_change():
    new_cit = st.session_state.citation
    old_sim = st.session_state.similarity
    old_court = st.session_state.court_stats
    remaining = 1 - new_cit
    old_sum = old_sim + old_court
    if old_sum == 0:
        st.session_state.similarity = remaining / 2
        st.session_state.court_stats = remaining / 2
    else:
        st.session_state.similarity = old_sim / old_sum * remaining
        st.session_state.court_stats = old_court / old_sum * remaining

    st.cache_data.clear()

def on_court_stats_change():
    new_court = st.session_state.court_stats
    old_sim = st.session_state.similarity
    old_cit = st.session_state.citation
    remaining = 1 - new_court
    old_sum = old_sim + old_cit
    if old_sum == 0:
        st.session_state.similarity = remaining / 2
        st.session_state.citation = remaining / 2
    else:
        st.session_state.similarity = old_sim / old_sum * remaining
        st.session_state.citation = old_cit / old_sum * remaining

    st.cache_data.clear()

def pdf_to_text(pdf_path):

    doc = fitz.open(stream=pdf_path.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# Define a helper function to close all summary/evaluation sections
def close_all():
    for key in st.session_state.keys():
        if key.startswith("show_summary_") or key.startswith("show_eval_"):
            st.session_state[key] = False


def validate_numeric_input(input):
    # Validate numeric input; if invalid, default to 1.
    try:
        num_docs = int(input)
        if num_docs < 0:
            st.sidebar.error("Please enter a a positive number.")
            return 1
        
        st.cache_data.clear()

        return num_docs
    
    except ValueError:
        st.sidebar.error("Please enter a valid number.")
        return 1
    

evaluation_template = """

**Dispute Summary:**

[Insert Dispute Summary]

---
**Factor 1: Purpose and Character of the Use**  
- **For Fair Use:**  
  [Insert supportive arguments, including whether the use is transformative, nonprofit, or educational. Include case law.]  
- **Against Fair Use:**  
  [Insert counterarguments, such as commercial nature or lack of transformation. Include case law.]

---
**Factor 2: Nature of the Copyrighted Work**  
- **For Fair Use:**  
  [Insert supportive arguments, e.g., factual vs. creative work, published status. Include case law.]  
- **Against Fair Use:**  
  [Insert counterarguments, such as if the work is highly creative or unpublished. Include case law.]

---
**Factor 3: Amount and Substantiality of the Portion Used**  
- **For Fair Use:**  
  [Discuss whether only a limited or necessary portion was used. Include case law.]  
- **Against Fair Use:**  
  [Discuss if the “heart” of the work or a substantial portion was taken. Include case law.]

---
**Factor 4: Effect of the Use Upon the Market**  
- **For Fair Use:**  
  [Explain why there is no significant harm to the market or potential licensing. Include case law.]  
- **Against Fair Use:**  
  [Explain how the use could harm the market or act as a substitute. Include case law.]

---
**Conclusion:**  
Weigh all four factors and conclude whether the use likely qualifies as fair use, does not qualify, or falls into a gray area. Provide a reasoned summary of the analysis.

Limit to a maximum of 1000 words

"""