import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from document_loader import load_document
from text_processor import process_documents
from vector_store import create_vector_store, add_documents_to_store
from ui_styles import inject_global_css

st.set_page_config(page_title="Upload Bills", page_icon="📤", layout="wide")
inject_global_css()

st.markdown('<h1 class="page-header">📤 Upload Billing Documents</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Upload your PDF bills, invoices, or billing statements. The assistant will extract and index the content for analysis.</p>', unsafe_allow_html=True)

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "uploaded_files_list" not in st.session_state:
    st.session_state.uploaded_files_list = []

uploaded_files = st.file_uploader(
    "Choose PDF or image files",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True,
    help="Upload one or more PDF billing documents or images of bills"
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.name in st.session_state.uploaded_files_list:
            st.info(f"✅ {uploaded_file.name} — already processed")
            continue
        with st.spinner(f"Processing {uploaded_file.name}..."):
            st.write(f"📄 Extracting text from {uploaded_file.name}...")
            raw_text = load_document(uploaded_file)
            if raw_text.startswith("Error"):
                st.error(f"❌ Failed to process {uploaded_file.name}: {raw_text}")
                continue
            st.write("✂️ Splitting text into chunks...")
            chunks = process_documents(raw_text)
            st.write(f"   → Created {len(chunks)} chunks")
            st.write("🧮 Generating embeddings and indexing...")
            if st.session_state.vector_store is None:
                st.session_state.vector_store = create_vector_store(chunks)
            else:
                st.session_state.vector_store = add_documents_to_store(
                    st.session_state.vector_store, chunks
                )
            st.session_state.uploaded_files_list.append(uploaded_file.name)
            st.success(f"✅ {uploaded_file.name} processed successfully!")
            with st.expander(f"Preview extracted text from {uploaded_file.name}"):
                st.text(raw_text[:2000])

st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)

if st.session_state.vector_store is not None:
    st.markdown(f"""
    <div class="glass-card">
        <h4>📊 Current Status</h4>
        <p><span class="status-success">●</span> <strong>{len(st.session_state.uploaded_files_list)}</strong> document(s) uploaded</p>
        <p><span class="status-info">●</span> Files: {', '.join(st.session_state.uploaded_files_list)}</p>
        <p><span class="status-success">●</span> Vector store ready for queries</p>
        <p style="color: #8892B0; margin-top: 0.8rem;">👉 Go to <strong>Chat with Bills</strong> to ask questions!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("👆 Upload a PDF to get started")