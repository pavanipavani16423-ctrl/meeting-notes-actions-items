import streamlit as st

st.set_page_config(page_title="Meeting Notes → Action Items", page_icon="📋")
st.title("📋 Meeting Notes → Action Items")
st.write("Paste your meeting notes and extract structured action items.")


def extract_action_items(meeting_notes: str):
    from model import ActionItemsOutput
    from parser import parser
    from prompt import get_prompt, get_llm

    try:
        from langfuse import get_client
        from langfuse.langchain import CallbackHandler
        langfuse = get_client()
        handler = CallbackHandler()
        use_langfuse = True
    except Exception as e:
        use_langfuse = False
        handler = None

    llm = get_llm()
    prompt = get_prompt()
    chain = prompt | llm | parser

    if use_langfuse and handler:
        result = chain.invoke(
            {"meeting_notes": meeting_notes},
            config={"callbacks": [handler]}
        )
    else:
        result = chain.invoke({"meeting_notes": meeting_notes})

    return result


meeting_notes_input = st.text_area(
    label="📝 Meeting Notes",
    placeholder="e.g. John will complete the dashboard by Friday.",
    height=220
)

if st.button("⚡ Extract Action Items"):
    if not meeting_notes_input.strip():
        st.warning("Please enter meeting notes before clicking Extract.")
    else:
        with st.spinner("Analyzing meeting notes, please wait..."):
            try:
                result = extract_action_items(meeting_notes_input.strip())
                st.success("Action items extracted successfully!")

                st.subheader("Action Items")
                for i, item in enumerate(result.actions, start=1):
                    priority_color = {
                        "High": "🔴", "Medium": "🟡", "Low": "🟢"
                    }.get(item.priority, "⚪")
                    with st.expander(
                        f"{priority_color} [{i}] {item.task}", expanded=True
                    ):
                        c1, c2, c3 = st.columns(3)
                        c1.metric("👤 Owner", item.owner)
                        c2.metric("📅 Deadline", item.deadline)
                        c3.metric("⚡ Priority", item.priority)

                st.divider()
                with st.expander("🔧 Raw JSON Output"):
                    st.json(result.model_dump())

                st.caption("🔭 LLM calls are traced in Langfuse dashboard.")

            except Exception as e:
                st.error(f"Something went wrong: {e}")