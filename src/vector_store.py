from langchain_community.vectorstores import FAISS
from embeddings import get_embedding_model

def create_vector_store(document_chunks):
    if not document_chunks:
        raise ValueError("No document chunks to index. The document may be empty or could not be processed.")

    embeddings = get_embedding_model()
    vector_store = FAISS.from_documents(document_chunks, embeddings)
    return vector_store

def get_retriever(vector_store, k=5):
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": k,
            "fetch_k": k * 3,
        }
    )
    return retriever

def add_documents_to_store(vector_store, new_chunks):
    if not new_chunks:
        return vector_store
    vector_store.add_documents(new_chunks)
    return vector_store