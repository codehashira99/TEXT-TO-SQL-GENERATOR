import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from core.sql_generator import generate_sql
from core.sql_validator import validate_sql
from core.query_executor import execute_query
from core.summarizer import summarize_results
from utils.history_logger import init_history, log_query, get_history

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Text-to-SQL AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .stTextArea textarea { font-size: 16px; border-radius: 10px; }
    .sql-box {
        background: #1e1e2e; color: #cdd6f4; padding: 16px;
        border-radius: 10px; font-family: monospace; font-size: 14px;
        border-left: 4px solid #89b4fa; white-space: pre-wrap;
    }
    .summary-box {
        background: #1e2e1e; color: #a6e3a1; padding: 16px;
        border-radius: 10px; font-size: 15px;
        border-left: 4px solid #a6e3a1;
    }
    .error-box {
        background: #2e1e1e; color: #f38ba8; padding: 12px;
        border-radius: 8px; border-left: 4px solid #f38ba8;
    }
    .metric-card {
        background: #1e1e2e; padding: 16px; border-radius: 10px;
        text-align: center; border: 1px solid #313244;
    }
    h1 { color: #cdd6f4 !important; }
</style>
""", unsafe_allow_html=True)

init_history()

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Text-to-SQL AI")
    st.markdown("Ask questions in plain English. Get SQL + insights instantly.")
    st.divider()
    
    st.markdown("### 💡 Sample Questions")
    samples = [
        "Top 5 customers by total order value?",
        "Show all completed orders in 2024",
        "Average product price by category",
        "Which products are low on stock (under 60 units)?",
        "How many orders per country?",
        "Most ordered products by quantity",
        "Customers who never placed an order",
        "Monthly revenue trend in 2024"
    ]
    for q in samples:
        if st.button(q, key=q, use_container_width=True):
            st.session_state.selected_query = q
    
    st.divider()
    st.markdown("### 📊 Database Schema")
    with st.expander("View Tables"):
        st.markdown("""
**customers** — name, email, city, country, signup_date  
**products** — name, category, price, stock_quantity  
**orders** — customer_id, order_date, status, total_amount  
**order_items** — order_id, product_id, quantity, unit_price
        """)

# ─── Main Content ──────────────────────────────────────────────────────────────
st.markdown("# 🧠 Natural Language → SQL")
st.markdown("Query your business database using plain English — no SQL knowledge needed.")
st.divider()

# Input
default_query = st.session_state.get("selected_query", "")
user_question = st.text_area(
    "Ask a question about your data:",
    value=default_query,
    placeholder="e.g. What are the top 5 customers by total order value?",
    height=80,
    key="question_input"
)

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    run_btn = st.button("🚀 Run Query", type="primary", use_container_width=True)
with col2:
    clear_btn = st.button("🗑️ Clear", use_container_width=True)

if clear_btn:
    st.session_state.selected_query = ""
    st.rerun()

# ─── Query Execution ───────────────────────────────────────────────────────────
if run_btn and user_question.strip():
    
    with st.spinner("🤖 Generating SQL..."):
        try:
            sql = generate_sql(user_question)
        except Exception as e:
            st.markdown(f'<div class="error-box">❌ LLM Error: {e}</div>', unsafe_allow_html=True)
            st.stop()
    
    # Show SQL
    st.markdown("### 📝 Generated SQL")
    st.markdown(f'<div class="sql-box">{sql}</div>', unsafe_allow_html=True)
    
    # Validate
    is_safe, val_error = validate_sql(sql)
    if not is_safe:
        st.markdown(f'<div class="error-box">🚫 Safety Check Failed: {val_error}</div>', unsafe_allow_html=True)
        log_query(user_question, sql, 0, False, val_error)
        st.stop()
    
    # Execute
    with st.spinner("⚙️ Executing query..."):
        df, exec_error = execute_query(sql)
    
    if exec_error:
        st.markdown(f'<div class="error-box">❌ Query Error: {exec_error}</div>', unsafe_allow_html=True)
        log_query(user_question, sql, 0, False, exec_error)
        st.stop()
    
    # Metrics row
    st.divider()
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Rows Returned", len(df))
    with m2:
        st.metric("Columns", len(df.columns))
    with m3:
        st.metric("Status", "✅ Success")
    
    # Results Table
    st.markdown("### 📊 Query Results")
    if df.empty:
        st.info("Query executed successfully but returned no rows.")
    else:
        st.dataframe(df, use_container_width=True, height=350)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button("⬇️ Download CSV", csv, "results.csv", "text/csv")
    
    # Summary
    if not df.empty:
        with st.spinner("✍️ Generating summary..."):
            summary = summarize_results(user_question, sql, df)
        st.markdown("### 💬 AI Summary")
        st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
    
    log_query(user_question, sql, len(df), True)

elif run_btn:
    st.warning("Please enter a question first.")

# ─── Query History ─────────────────────────────────────────────────────────────
history = get_history()
if history:
    st.divider()
    st.markdown("### 🕓 Query History")
    for i, entry in enumerate(reversed(history[-10:])):
        icon = "✅" if entry["success"] else "❌"
        with st.expander(f"{icon} [{entry['timestamp']}] {entry['question'][:60]}..."):
            st.code(entry["sql"], language="sql")
            if entry["success"]:
                st.caption(f"Returned {entry['row_count']} rows")
            else:
                st.caption(f"Error: {entry['error']}")