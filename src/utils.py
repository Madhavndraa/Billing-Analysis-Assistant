import streamlit as st
def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "vector_store": None,
        "uploaded_files_list": [],
        "chat_history": [],
        "qa_chain": None,
        "bill_summary": None,
        "anomaly_report": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
def format_sources(source_documents):
    """Format source documents for display."""
    formatted = []
    for i, doc in enumerate(source_documents):
        formatted.append(f"**Source {i+1}:** {doc.page_content[:200]}...")
    return "\n\n".join(formatted)
