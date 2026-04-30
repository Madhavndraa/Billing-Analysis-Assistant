import streamlit as st

def inject_global_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        .stApp { font-family: 'Inter', sans-serif; }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0d0f1a 0%, #111428 100%);
            border-right: 1px solid rgba(102, 126, 234, 0.12);
        }
        .stApp > header { background: transparent; }

        .page-header {
            font-family: 'Inter', sans-serif;
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 0.3rem 0;
            letter-spacing: -0.02em;
        }
        .page-subtitle {
            color: #8892B0;
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
            line-height: 1.6;
        }
        .divider-glow {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.25), rgba(168, 85, 247, 0.25), transparent);
            margin: 1.5rem 0;
            border: none;
        }
        .glass-card {
            background: rgba(17, 20, 40, 0.5);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid rgba(102, 126, 234, 0.1);
            border-top: 1px solid rgba(255, 255, 255, 0.04);
            margin-bottom: 1rem;
        }
        .glass-card h4 {
            color: #e2e8f0;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .status-success {
            color: #4ade80;
            font-weight: 600;
        }
        .status-info {
            color: #667eea;
            font-weight: 500;
        }

        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.3s ease !important;
        }
        .stButton > button:hover {
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.35) !important;
            transform: translateY(-2px) !important;
        }

        div[data-testid="stMetric"] {
            background: rgba(17, 20, 40, 0.5);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(102, 126, 234, 0.1);
            border-radius: 14px;
            padding: 1rem 1.2rem;
        }
        div[data-testid="stMetric"] label {
            color: #8892B0 !important;
            font-size: 0.78rem !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.06em !important;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #e2e8f0 !important;
            font-weight: 700 !important;
        }

        div[data-testid="stExpander"] {
            background: rgba(17, 20, 40, 0.4);
            border: 1px solid rgba(102, 126, 234, 0.1);
            border-radius: 12px;
        }

        .stChatMessage {
            border-radius: 14px !important;
        }
        div[data-testid="stChatInput"] > div {
            border-radius: 14px !important;
            border-color: rgba(102, 126, 234, 0.2) !important;
        }

        .stDataFrame {
            border-radius: 12px;
            overflow: hidden;
        }
    </style>
    """, unsafe_allow_html=True)
