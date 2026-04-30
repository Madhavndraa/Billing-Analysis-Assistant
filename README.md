# 💰 Billing Analysis Assistant

An AI-powered billing analysis tool that lets you upload invoices, ask questions in plain English, and get instant answers with interactive charts and anomaly detection.

Built with **LangChain**, **Streamlit**, **Groq (Llama 4 Scout)**, and **FAISS**.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **📤 Upload Bills** | Upload PDF invoices or receipt images (JPG/PNG). Supports multi-file upload. |
| **💬 Chat with Bills** | Ask billing questions in plain English — get accurate, source-referenced answers. |
| **📊 Smart Dashboard** | Auto-generated Plotly charts (bar + pie), key metrics, line item tables, and AI summaries. |
| **🔍 Anomaly Detection** | AI forensic auditor that flags hidden fees, duplicate charges, and math errors. |
| **🖼️ Image Extraction** | Multimodal Vision LLM reads crumpled receipts without traditional OCR. |

---

## 🏗️ Architecture

```
User uploads PDF/Image
        ↓
┌─────────────────────────────────────┐
│  Document Extraction                │
│  pdfplumber (tables) → PyPDF2 (fb) │
│  OR Base64 → Groq Vision LLM       │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Text Processing                    │
│  Regex cleaning → Chunking (800/150)│
│  RecursiveCharacterTextSplitter     │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Embedding & Indexing               │
│  HuggingFace all-MiniLM-L6-v2      │
│  → FAISS Vector Store (in-memory)   │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  RAG Pipeline (LangChain LCEL)      │
│  MMR Retrieval (k=5, fetch_k=15)   │
│  → Prompt Template → Groq LLM      │
│  → StrOutputParser                  │
└──────────────┬──────────────────────┘
               ↓
        Streamlit UI
```

---

## 🛠️ Tech Stack

| Component | Technology | Why This? |
|-----------|-----------|-----------|
| **Frontend** | Streamlit | Rapid Python-native UI for AI apps |
| **LLM** | Groq (Llama 4 Scout 17B) | Free, ultra-fast inference via LPU hardware |
| **Embeddings** | HuggingFace (all-MiniLM-L6-v2) | Runs 100% locally on CPU — zero cost, private |
| **Vector DB** | FAISS | In-memory, fastest similarity search, zero setup |
| **RAG Framework** | LangChain (LCEL) | Modern expression language, modular pipelines |
| **PDF Parsing** | pdfplumber + PyPDF2 | Table-aware extraction with fallback |
| **Charts** | Plotly | Interactive, JavaScript-rendered visualizations |
| **Image OCR** | Groq Vision LLM | Context-aware extraction, no Tesseract needed |

---

## 📁 Project Structure

```
Billing Analysis Assistant/
├── app.py                     # Home page + navigation
├── pages/
│   ├── 1_Upload_Bills.py      # File upload & processing
│   ├── 2_Chat_with_Agent.py   # RAG chat interface
│   ├── 3_Dashboard.py         # Charts & metrics
│   └── 4_Anamoly_Detection.py # Anomaly analysis
├── src/
│   ├── document_loader.py     # PDF/Image text extraction
│   ├── text_processor.py      # Cleaning & chunking
│   ├── embeddings.py          # HuggingFace local model
│   ├── vector_store.py        # FAISS creation & retrieval
│   ├── rag_chain.py           # LangChain LCEL pipelines
│   ├── prompts.py             # All prompt templates
│   └── ui_styles.py           # Shared premium CSS
├── evaluation/
│   ├── evaluate.py            # Automated test runner
│   └── eval_results.json      # Performance metrics
├── .streamlit/
│   ├── config.toml            # Streamlit config
│   └── secrets.toml           # API keys (not committed)
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- A free [Groq API Key](https://console.groq.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Billing-Analysis-Assistant.git
cd Billing-Analysis-Assistant

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Add your API key
mkdir .streamlit
echo 'GROQ_API_KEY = "gsk_your_key_here"' > .streamlit/secrets.toml

# Run the app
streamlit run app.py
```

---

## 📊 Evaluation Results

The system was tested against 15 financial scenarios:

| Category | Accuracy | Notes |
|----------|----------|-------|
| **Amount Extraction** | 93.3% | Totals, taxes, line items |
| **Summarization** | 100% | Bill summaries |
| **Billing Period** | 80% | Date extraction |
| **Anomaly Detection** | 40% | Requires more context |
| **Overall** | 62.9% | Keyword-match scoring (strict) |

> **Note:** The 62.9% reflects strict keyword matching. Semantic accuracy (judged by humans) is significantly higher — the AI gives correct answers that don't always contain the exact expected keywords.

---

## 🔑 Key Technical Decisions

- **MMR over Similarity Search** — Prevents duplicate chunks from flooding the LLM context
- **Chunk Size 800 / Overlap 150** — Optimized for dense financial documents
- **Dual PDF Extractors** — pdfplumber for tables, PyPDF2 as fallback for corrupted files
- **Local Embeddings** — Financial documents never leave your machine during embedding
- **Exponential Backoff** — `_safe_invoke()` retries on 429 rate limits (3s, 6s, 9s)
- **LCEL Syntax** — Uses modern LangChain Expression Language, not deprecated chains

---

## 📜 License

This project is for educational purposes.

---

## 🙏 Acknowledgments

- [LangChain](https://langchain.com) — RAG framework
- [Groq](https://groq.com) — Free LLM inference
- [HuggingFace](https://huggingface.co) — Local embedding model
- [Streamlit](https://streamlit.io) — Python web framework
