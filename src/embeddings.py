from langchain_huggingface import HuggingFaceEmbeddings
import streamlit as st


@st.cache_resource 
def get_embedding_model():
    """
    Load the HuggingFace embedding model.

    Uses 'all-MiniLM-L6-v2' which:
    - Runs 100% locally (no API calls)
    - Produces 384-dimensional vectors
    - Is fast and lightweight
    - Works within Streamlit Cloud's 1GB RAM
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},  
        encode_kwargs={'normalize_embeddings': True}
    )
    return embeddings
