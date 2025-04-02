import streamlit as st

# ----- Initialization of Session State Variables -----
if "email" not in st.session_state:
    st.session_state.email = None
if "current_item" not in st.session_state:
    st.session_state.current_item = 0
if "responses" not in st.session_state:
    st.session_state.responses = {}

TOTAL_ITEMS = 5  # Number of items (adjust as needed)

# ----- User Identification (Email Entry) -----
if st.session_state.email is None:
    st.markdown("### Please Enter Your Email to Continue")
    email_input = st.text_input("Email:")
    if st.button("Submit"):
        if email_input.strip():
            st.session_state.email = email_input.strip()
            # Here you could load previous session data from a DB if available.
        else:
            st.error("A valid email is required to proceed.")
    st.stop()

# ----- Main App Interface for Rating Items -----
st.markdown(f"### Item {st.session_state.current_item + 1} of {TOTAL_ITEMS}")

# --- Full-width Context Panel ---
context_text = "This is some placeholder context text. " * 20
st.markdown("#### Context")
st.write(context_text)

# --- Left and Right Text Panels ---
left_text = "This is the left panel placeholder text. " * 20
right_text = "This is the right panel placeholder text. " * 20

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Left Text")
    st.text_area("Left Panel", value=left_text, height=300, key="left_text_area")
with col2:
    st.markdown("#### Right Text")
    st.text_area("Right Panel", value=right_text, height=300, key="right_text_area")

# --- Rating Section ---
st.markdown("#### Rate the Texts")
overall_preference = st.radio("Overall Preference", options=["Left", "Right"])
left_score = st.slider("Score for Left Text (0-10)", 0, 10, 5, key="left_score")
right_score = st.slider("Score for Right Text (0-10)", 0, 10, 5, key="right_score")

# --- Next Button to Save Response and Move Forward ---
if st.button("Next"):
    # Save the responses for the current item
    st.session_state.responses[st.session_state.current_item] = {
        "overall_preference": overall_preference,
        "left_score": left_score,
        "right_score": right_score,
        "email": st.session_state.email,
    }
    st.session_state.current_item += 1

    # Check if all items are completed
    if st.session_state.current_item >= TOTAL_ITEMS:
        st.success("Thank you for completing all items!")
        st.write("Your responses:", st.session_state.responses)
        st.stop()
    else:
        # Check if experimental_rerun exists; if not, prompt the user to refresh
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.write("Please refresh the page to continue.")
