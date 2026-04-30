import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

st.set_page_config(
    page_title="Billing Analysis Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ===== GLOBAL OVERRIDES ===== */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0f1a 0%, #111428 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.12);
    }
    .stApp > header { background: transparent; }

    /* ===== HERO SECTION ===== */
    .hero-badge {
        display: inline-block;
        background: rgba(102, 126, 234, 0.12);
        border: 1px solid rgba(102, 126, 234, 0.25);
        border-radius: 999px;
        padding: 0.4rem 1.2rem;
        font-size: 0.8rem;
        font-weight: 600;
        color: #b9c3ff;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 0.5rem 0;
        letter-spacing: -0.03em;
        line-height: 1.15;
    }
    .sub-header {
        text-align: center;
        font-size: 1.1rem;
        color: #8892B0;
        margin-bottom: 2.5rem;
        font-family: 'Inter', sans-serif;
        line-height: 1.7;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }

    /* ===== FEATURE CARDS ===== */
    .feature-card {
        background: rgba(17, 20, 40, 0.6);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 2rem 1.6rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(102, 126, 234, 0.12);
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        min-height: 220px;
        position: relative;
        overflow: hidden;
    }
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #a855f7);
        opacity: 0;
        transition: opacity 0.35s ease;
    }
    .feature-card:hover {
        transform: translateY(-6px);
        border-color: rgba(102, 126, 234, 0.3);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.12),
                    0 0 60px rgba(102, 126, 234, 0.05);
    }
    .feature-card:hover::before { opacity: 1; }
    .feature-icon {
        font-size: 2.4rem;
        margin-bottom: 0.8rem;
        display: block;
    }
    .feature-card h3 {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
        color: #e2e8f0;
    }
    .feature-card p {
        color: #8892B0;
        font-size: 0.88rem;
        line-height: 1.65;
    }

    /* ===== STEP CARDS ===== */
    .step-card {
        background: rgba(17, 20, 40, 0.4);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 1.8rem 1.2rem;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.08);
        transition: all 0.3s ease;
    }
    .step-card:hover {
        border-color: rgba(102, 126, 234, 0.2);
        transform: translateY(-3px);
    }
    .step-number {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #667eea, #a855f7);
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 0.8rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .step-label {
        font-size: 0.85rem;
        color: #c5c5d5;
        font-weight: 500;
    }
    .step-arrow {
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(102, 126, 234, 0.4);
        font-size: 1.5rem;
    }

    /* ===== DIVIDERS ===== */
    .divider-glow {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.25), rgba(168, 85, 247, 0.25), transparent);
        margin: 2.5rem 0;
        border: none;
    }
    .section-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #c5c5d5;
        margin-bottom: 1.5rem;
    }

    /* ===== TECH BADGE ===== */
    .tech-stack {
        display: flex;
        justify-content: center;
        gap: 0.6rem;
        flex-wrap: wrap;
        margin-top: 1.5rem;
    }
    .tech-badge {
        background: rgba(102, 126, 234, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.15);
        border-radius: 999px;
        padding: 0.3rem 0.8rem;
        font-size: 0.72rem;
        font-weight: 500;
        color: #8892B0;
        letter-spacing: 0.02em;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
        font-size: 0.85rem !important;
    }
    .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35) !important;
        transform: translateY(-2px) !important;
    }

    /* ===== SIDEBAR ===== */
    .sidebar-brand {
        text-align: center;
        padding: 0.5rem 0 1rem 0;
    }
    .sidebar-brand-icon {
        font-size: 2.5rem;
        display: block;
        margin-bottom: 0.3rem;
    }
    .sidebar-brand-text {
        font-size: 1rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center;">
    <span class="hero-badge">⚡ AI-Powered Financial Intelligence</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">💰 Billing Analysis<br>Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload your bills, invoices, and billing documents — then ask questions in plain English.<br>Powered by <strong>RAG</strong> (Retrieval-Augmented Generation) & <strong>Llama 4</strong>.</p>', unsafe_allow_html=True)

st.markdown("""
<div class="tech-stack">
    <span class="tech-badge">🧠 LangChain</span>
    <span class="tech-badge">⚡ Groq LPU</span>
    <span class="tech-badge">🦙 Llama 4 Scout</span>
    <span class="tech-badge">📦 FAISS</span>
    <span class="tech-badge">🤗 HuggingFace</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">📤</span>
        <h3>Upload Bills</h3>
        <p>Upload PDF bills and invoice images. AI extracts text, tables, and line items automatically.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Upload →", key="nav_upload", use_container_width=True):
        st.switch_page("pages/1_Upload_Bills.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">💬</span>
        <h3>Chat with Bills</h3>
        <p>Ask questions in plain English. Get accurate answers backed by source references.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Chat →", key="nav_chat", use_container_width=True):
        st.switch_page("pages/2_Chat_with_Agent.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">📊</span>
        <h3>Smart Dashboard</h3>
        <p>Auto-generated summaries with interactive Plotly charts, key metrics, and trends.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Dashboard →", key="nav_dash", use_container_width=True):
        st.switch_page("pages/3_Dashboard.py")

with col4:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🔍</span>
        <h3>Anomaly Detection</h3>
        <p>AI forensic auditor detects hidden fees, duplicate charges, and overcharges.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Anomaly →", key="nav_anomaly", use_container_width=True):
        st.switch_page("pages/4_Anamoly_Detection.py")

st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)

st.markdown('<p class="section-title">🔄 How It Works</p>', unsafe_allow_html=True)

c1, a1, c2, a2, c3, a3, c4 = st.columns([3, 1, 3, 1, 3, 1, 3])

with c1:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">1</div><br>
        <span class="step-label">Upload PDF or Image</span>
    </div>
    """, unsafe_allow_html=True)

with a1:
    st.markdown('<div class="step-arrow">→</div>', unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">2</div><br>
        <span class="step-label">AI Extracts & Indexes</span>
    </div>
    """, unsafe_allow_html=True)

with a2:
    st.markdown('<div class="step-arrow">→</div>', unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">3</div><br>
        <span class="step-label">Ask Questions</span>
    </div>
    """, unsafe_allow_html=True)

with a3:
    st.markdown('<div class="step-arrow">→</div>', unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">4</div><br>
        <span class="step-label">Get Smart Answers</span>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span class="sidebar-brand-icon">💰</span>
        <span class="sidebar-brand-text">Billing Assistant</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 📌 Quick Start")
    st.markdown("""
    1. Go to **📤 Upload Bills**
    2. Upload your PDF/image bill
    3. Go to **💬 Chat with Agent**
    4. Ask any question about your bill!
    """)

    st.divider()

    st.markdown("### 🛠️ Tech Stack")
    st.markdown("""
    - **LLM**: Groq (Llama 4 Scout)
    - **Embeddings**: HuggingFace (Local)
    - **Vector DB**: FAISS
    - **Framework**: LangChain + Streamlit
    """)

    st.divider()

    st.markdown("### 🔑 API Status")
    if "GROQ_API_KEY" in st.secrets:
        st.success("✅ Groq API Key configured")
    else:
        st.error("❌ Groq API Key missing — add to `.streamlit/secrets.toml`")

    if "vector_store" in st.session_state and st.session_state.vector_store is not None:
        st.info(f"📄 {len(st.session_state.get('uploaded_files_list', []))} document(s) loaded")
    else:
        st.info("📄 No documents loaded yet")
