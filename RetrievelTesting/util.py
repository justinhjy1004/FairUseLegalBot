import streamlit as st

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
