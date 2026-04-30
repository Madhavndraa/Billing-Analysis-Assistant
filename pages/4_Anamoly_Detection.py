import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rag_chain import detect_anomalies, APIKeyError, RateLimitError, LLMError
from ui_styles import inject_global_css

st.set_page_config(page_title="Anomaly Detection", page_icon="🔍", layout="wide")
inject_global_css()

st.markdown('<h1 class="page-header">🔍 Anomaly Detection</h1>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Automatically detect unusual charges, hidden fees, and billing anomalies using AI forensic analysis.</p>', unsafe_allow_html=True)

if "vector_store" not in st.session_state or st.session_state.vector_store is None:
    st.warning("⚠️ No documents uploaded yet! Please go to **Upload Bills** page first.")
    st.stop()

if "anomaly_report" not in st.session_state:
    st.session_state.anomaly_report = None

st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)

if st.button("🔍 Run Anomaly Analysis", type="primary", use_container_width=True):
    with st.spinner("Analyzing billing documents for anomalies..."):
        try:
            st.session_state.anomaly_report = detect_anomalies(st.session_state.vector_store)
        except RateLimitError as e:
            st.warning(f"⏳ {str(e)}")
        except APIKeyError as e:
            st.error(f"🔑 {str(e)}")
        except LLMError as e:
            st.error(f"❌ {str(e)}")
        except Exception as e:
            st.error(f"❌ Anomaly detection failed: {str(e)}")

if st.session_state.anomaly_report:
    st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)
    st.markdown("### 📋 Anomaly Analysis Report")
    st.markdown(f"""
    <div class="glass-card">
        {st.session_state.anomaly_report}
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 3rem;">
        <p style="font-size: 3rem; margin-bottom: 0.5rem;">🕵️</p>
        <p style="color: #8892B0; font-size: 1rem;">Click the button above to run anomaly detection on your uploaded bills.</p>
    </div>
    """, unsafe_allow_html=True)