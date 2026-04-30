import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rag_chain import get_qa_chain, ask_question, APIKeyError, RateLimitError, LLMError
from ui_styles import inject_global_css

st.set_page_config(page_title="Chat with Bills", page_icon="💬", layout="wide")
inject_global_css()

st.markdown('<h1 class="page-header">💬 Chat with Your Bills</h1>', unsafe_allow_html=True)

if "vector_store" not in st.session_state or st.session_state.vector_store is None:
    st.warning("⚠️ No documents uploaded yet! Please go to **Upload Bills** page first.")
    st.stop()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "qa_chain" not in st.session_state:
    try:
        st.session_state.qa_chain = get_qa_chain(st.session_state.vector_store)
    except APIKeyError as e:
        st.error(f"🔑 {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Failed to initialize chat: {str(e)}")
        st.stop()

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if len(st.session_state.chat_history) == 0:
    st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)
    st.markdown("### 💡 Try asking:")
    suggestions = [
        "What is the total amount of my bill?",
        "What are the main charges?",
        "What is the billing period?",
        "Are there any unusual or high charges?",
        "Summarize my bill in simple terms",
    ]
    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        if cols[i].button(suggestion, key=f"suggestion_{i}", use_container_width=True):
            st.session_state.pending_question = suggestion
            st.rerun()

if "pending_question" in st.session_state:
    question = st.session_state.pending_question
    del st.session_state.pending_question
else:
    question = None

user_input = st.chat_input("Ask a question about your bills...")

query = user_input or question

if query:
    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing your bills..."):
            try:
                import time
                start_time = time.time()
                response = ask_question(st.session_state.qa_chain, query)
                elapsed = time.time() - start_time

                answer = response["result"]
                sources = response.get("source_documents", [])
                st.markdown(answer)
                st.caption(f"⏱️ Response time: {elapsed:.2f}s")

                if sources:
                    with st.expander("📄 Source References"):
                        for i, doc in enumerate(sources):
                            st.markdown(f"**Chunk {i+1}:**")
                            st.text(doc.page_content[:300])
                            st.divider()

            except RateLimitError as e:
                answer = f"⏳ {str(e)}"
                st.warning(answer)

            except APIKeyError as e:
                answer = f"🔑 {str(e)}"
                st.error(answer)

            except LLMError as e:
                answer = f"❌ {str(e)}"
                st.error(answer)

            except Exception as e:
                answer = f"❌ An unexpected error occurred: {str(e)}"
                st.error(answer)

    st.session_state.chat_history.append({"role": "assistant", "content": answer})