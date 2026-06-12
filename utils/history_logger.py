import streamlit as st
from datetime import datetime

def init_history():
    if "query_history" not in st.session_state:
        st.session_state.query_history = []

def log_query(question: str, sql: str, row_count: int, success: bool, error: str = ""):
    init_history()
    st.session_state.query_history.append({
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "question": question,
        "sql": sql,
        "row_count": row_count,
        "success": success,
        "error": error
    })

def get_history():
    init_history()
    return st.session_state.query_history