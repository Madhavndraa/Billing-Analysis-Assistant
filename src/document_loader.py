import PyPDF2
import pdfplumber
from langchain_groq import ChatGroq
import streamlit as st
import base64

MAX_PDF_SIZE_MB = 20
MAX_IMAGE_SIZE_MB = 10

def validate_file(uploaded_file):
    filename = uploaded_file.name.lower()

    allowed_extensions = ('.pdf', '.png', '.jpg', '.jpeg')
    if not filename.endswith(allowed_extensions):
        return False, f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"

    uploaded_file.seek(0, 2)
    file_size_mb = uploaded_file.tell() / (1024 * 1024)
    uploaded_file.seek(0)

    if filename.endswith('.pdf') and file_size_mb > MAX_PDF_SIZE_MB:
        return False, f"PDF too large ({file_size_mb:.1f}MB). Maximum is {MAX_PDF_SIZE_MB}MB."

    if filename.endswith(('.png', '.jpg', '.jpeg')) and file_size_mb > MAX_IMAGE_SIZE_MB:
        return False, f"Image too large ({file_size_mb:.1f}MB). Maximum is {MAX_IMAGE_SIZE_MB}MB."

    if file_size_mb == 0:
        return False, "File is empty (0 bytes)."

    return True, ""

def extract_text_with_pypdf2(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        if len(pdf_reader.pages) == 0:
            return ""

        text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- Page {page_num+1} ---\n"
                text += page_text
        return text
    except Exception as e:
        return f"Error with PyPDF2: {str(e)}"

def extract_text_with_pdfplumber(pdf_file):
    try:
        text = ""
        with pdfplumber.open(pdf_file) as file:
            if len(file.pages) == 0:
                return ""

            for page_num, page in enumerate(file.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {page_num+1} ---\n"
                    text += page_text

                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        row_text = " | ".join([str(cell) if cell else "" for cell in row])
                        text += row_text + "\n"
        return text
    except Exception as e:
        return f"Error with pdfplumber: {str(e)}"

def load_document(uploaded_file):
    is_valid, error_msg = validate_file(uploaded_file)
    if not is_valid:
        return f"Error: {error_msg}"

    filename = uploaded_file.name.lower()

    if filename.endswith((".png", ".jpg", ".jpeg")):
        return extract_text_from_image(uploaded_file)

    try:
        uploaded_file.seek(0)
        text = extract_text_with_pdfplumber(uploaded_file)

        if len(text.strip()) < 50:
            uploaded_file.seek(0)
            text = extract_text_with_pypdf2(uploaded_file)

        text = text.strip()
        if len(text) < 20:
            return "Error: Could not extract meaningful text from this PDF. It may be a scanned image — try uploading as an image file instead."

        return text

    except Exception as e:
        return f"Error: Failed to process PDF — {str(e)}"

def extract_text_from_image(image_file):
    try:
        if "GROQ_API_KEY" not in st.secrets or not st.secrets["GROQ_API_KEY"]:
            return "Error: Groq API key not configured. Add it to `.streamlit/secrets.toml`."

        image_file.seek(0)
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

        if len(image_data) > 4 * 1024 * 1024:
            return "Error: Image too large for AI processing. Please resize it to under 4MB."

        from langchain_core.messages import HumanMessage

        llm = ChatGroq(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            api_key=st.secrets["GROQ_API_KEY"],
            timeout=30,
        )

        message = HumanMessage(
            content=[
                {"type": "text", "text": "Extract ALL text from this billing document image. Include every amount, date, line item, charge, and detail. Format it clearly."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
            ]
        )

        response = llm.invoke([message])
        text = response.content.strip()

        if len(text) < 20:
            return "Error: Could not extract meaningful text from this image. The image may be too blurry or unclear."

        return text

    except Exception as e:
        error_msg = str(e).lower()
        if "rate_limit" in error_msg or "429" in error_msg:
            return "Error: Rate limit exceeded. Groq free tier allows 30 requests/minute. Please wait and try again."
        elif "auth" in error_msg or "401" in error_msg:
            return "Error: Invalid Groq API key. Please check `.streamlit/secrets.toml`."
        elif "timeout" in error_msg:
            return "Error: Request timed out. The server may be busy — please try again."
        else:
            return f"Error: Failed to process image — {str(e)}"
