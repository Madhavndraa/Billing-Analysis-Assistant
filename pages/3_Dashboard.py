import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rag_chain import get_summary, get_chart_data, APIKeyError, RateLimitError, LLMError
from ui_styles import inject_global_css
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
inject_global_css()

st.markdown('<h1 class="page-header">📊 Billing Dashboard</h1>', unsafe_allow_html=True)

if "vector_store" not in st.session_state or st.session_state.vector_store is None:
    st.warning("⚠️ No documents uploaded yet! Please go to **Upload Bills** page first.")
    st.stop()

st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)

if "chart_data" not in st.session_state:
    with st.spinner("📊 Extracting billing data for charts..."):
        try:
            st.session_state.chart_data = get_chart_data(st.session_state.vector_store)
        except APIKeyError as e:
            st.error(f"🔑 {str(e)}")
            st.session_state.chart_data = None
        except RateLimitError as e:
            st.warning(f"⏳ {str(e)}")
            st.session_state.chart_data = None
        except (LLMError, Exception) as e:
            st.error(f"❌ Could not generate chart data: {str(e)}")
            st.session_state.chart_data = None

chart_data = st.session_state.chart_data

if chart_data:
    currency = chart_data.get("currency", "$")
    total = chart_data.get("total_amount", 0)
    tax = chart_data.get("tax_amount", 0)
    subtotal = chart_data.get("subtotal", total - tax if total and tax else 0)
    items = chart_data.get("items", [])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Amount", f"{currency}{total:,.2f}")
    with col2:
        st.metric("Tax", f"{currency}{tax:,.2f}")
    with col3:
        st.metric("Subtotal", f"{currency}{subtotal:,.2f}")
    with col4:
        st.metric("Line Items", len(items))

    st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)

    if items and len(items) > 0:
        st.markdown("### 📊 Billing Breakdown")

        col_bar, col_pie = st.columns(2)

        with col_bar:
            item_names = [item.get("name", "Unknown")[:25] for item in items]
            item_amounts = [float(item.get("amount", 0)) for item in items]

            fig_bar = go.Figure(data=[
                go.Bar(
                    x=item_names,
                    y=item_amounts,
                    marker_color=['#667eea', '#a855f7', '#ec4899', '#f97316', '#22d3ee', '#4ade80', '#facc15'][:len(items)],
                    text=[f"{currency}{a:,.2f}" for a in item_amounts],
                    textposition='outside',
                    textfont=dict(size=11, family='Inter'),
                )
            ])
            fig_bar.update_layout(
                title=dict(text="Charge Breakdown by Item", font=dict(family='Inter', size=16, color='#c5c5d5')),
                xaxis_title="Items",
                yaxis_title=f"Amount ({currency})",
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=420,
                margin=dict(t=50, b=80),
                xaxis_tickangle=-30,
                font=dict(family='Inter', color='#8892B0'),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_pie:
            pie_labels = item_names + ["Tax"]
            pie_values = item_amounts + [float(tax)]

            fig_pie = go.Figure(data=[
                go.Pie(
                    labels=pie_labels,
                    values=pie_values,
                    hole=0.45,
                    textinfo='label+percent',
                    textfont=dict(size=11, family='Inter'),
                    marker=dict(
                        colors=['#667eea', '#a855f7', '#ec4899', '#f97316', '#22d3ee', '#4ade80', '#facc15', '#ef4444'][:len(pie_labels)],
                        line=dict(color='#121319', width=2)
                    ),
                )
            ])
            fig_pie.update_layout(
                title=dict(text="Charge Distribution", font=dict(family='Inter', size=16, color='#c5c5d5')),
                template="plotly_dark",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                height=420,
                margin=dict(t=50, b=40),
                showlegend=True,
                legend=dict(font=dict(size=10, family='Inter', color='#8892B0')),
                font=dict(family='Inter', color='#8892B0'),
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)
        st.markdown("### 📋 Line Items Detail")

        table_data = []
        for item in items:
            table_data.append({
                "Item": item.get("name", "Unknown"),
                "Qty": item.get("quantity", 1),
                "Amount": f"{currency}{float(item.get('amount', 0)):,.2f}",
            })

        st.dataframe(table_data, use_container_width=True, hide_index=True)

        seller = chart_data.get("seller", "")
        buyer = chart_data.get("buyer", "")
        inv_num = chart_data.get("invoice_number", "")
        date = chart_data.get("date", "")

        if any([seller, buyer, inv_num, date]):
            st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)
            st.markdown("### 🏢 Invoice Details")
            col1, col2 = st.columns(2)
            with col1:
                if seller:
                    st.markdown(f"**Seller:** {seller}")
                if inv_num:
                    st.markdown(f"**Invoice #:** {inv_num}")
            with col2:
                if buyer:
                    st.markdown(f"**Buyer:** {buyer}")
                if date:
                    st.markdown(f"**Date:** {date}")

else:
    st.info("📊 Could not extract structured data for charts. See the text summary below.")

st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)
st.markdown("### 📋 AI-Generated Summary")

if "bill_summary" not in st.session_state:
    with st.spinner("Generating billing summary..."):
        try:
            st.session_state.bill_summary = get_summary(st.session_state.vector_store)
        except RateLimitError as e:
            st.session_state.bill_summary = f"⏳ {str(e)}"
        except (APIKeyError, LLMError, Exception) as e:
            st.session_state.bill_summary = f"❌ Could not generate summary: {str(e)}"

st.markdown(st.session_state.bill_summary)

if st.button("🔄 Refresh All Data", type="primary"):
    with st.spinner("Regenerating dashboard..."):
        try:
            st.session_state.bill_summary = get_summary(st.session_state.vector_store)
            st.session_state.chart_data = get_chart_data(st.session_state.vector_store)
        except RateLimitError as e:
            st.warning(f"⏳ {str(e)}")
        except Exception as e:
            st.error(f"❌ Refresh failed: {str(e)}")
    st.rerun()

st.markdown('<div class="divider-glow"></div>', unsafe_allow_html=True)

st.markdown("### 📁 Upload Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Documents Uploaded",
        value=len(st.session_state.get("uploaded_files_list", []))
    )

with col2:
    if st.session_state.vector_store is not None:
        st.metric(
            label="Total Chunks Indexed",
            value=st.session_state.vector_store.index.ntotal
        )

with col3:
    st.metric(
        label="Questions Asked",
        value=len(st.session_state.get("chat_history", [])) // 2
    )