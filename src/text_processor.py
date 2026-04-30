import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

DEFAULT_CHUNK_SIZE = 800
DEFAULT_CHUNK_OVERLAP = 150

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\,\.\;\:\@\-\!\?\/\|\(\)\#\$\%\&\₹\€\£\+\=\*]', '', text)
    lines = text.split('\n')
    lines = [line.strip() for line in lines if len(line.strip()) > 10]
    text = '\n'.join(lines)
    return text.strip()

def chunk_text(text, chunk_size=DEFAULT_CHUNK_SIZE, chunk_overlap=DEFAULT_CHUNK_OVERLAP):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=['\n\n', '\n', '. ', ' ', '']
    )
    chunks = text_splitter.create_documents([text])
    return chunks

def process_documents(text):
    cleaned = clean_text(text)
    if len(cleaned) < 50:
        from langchain_core.documents import Document
        return [Document(page_content=cleaned)] if cleaned else []
    chunks = chunk_text(cleaned)
    return chunks