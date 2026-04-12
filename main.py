import streamlit as st
from model import get_llm_response
from parser import parse_output

# Page config
st.set_page_config(page_title="Meeting Notes → Action Items", layout="centered")

st.title("📝 Meeting Notes → Action Items")

# Input box
user_input = st.text_area("Enter Meeting Notes", height=200)

# 🔘 Test case buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Load Test Case 1"):
        user_input = """John will complete the dashboard by Friday.
Sarah will review the data.
Prepare final presentation before Monday."""

with col2:
    if st.button("Load Test Case 2"):
        user_input = """Prepare project documentation before Wednesday.
Finalize UI design by Friday."""

with col3:
    if st.button("Load Test Case 3"):
        user_input = """Ravi will update the database.
Anita will test the application."""

# Show updated input
st.text_area("Loaded Notes", value=user_input, height=200)

# 🚀 Analyze button (YOUR CODE ADDED)
if st.button("Analyze"):

    if not user_input.strip():
        st.warning("Please enter meeting notes")
    else:
        response = get_llm_response(user_input)

        result = parse_output(user_input)
        # 🔍 Debug (optional)
        st.write(result)

        if not result["actions"]:
            st.warning("No action items found")

        else:
            st.success("Extraction Successful")

            for i, action in enumerate(result["actions"], 1):
                st.subheader(f"Task {i}")
                st.write(f"Task: {action['task']}")
                st.write(f"Owner: {action['owner']}")
                st.write(f"Deadline: {action['deadline']}")
                st.write(f"Priority: {action['priority']}")
                st.divider()