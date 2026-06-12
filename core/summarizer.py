from core.llm_client import call_llm
import pandas as pd

SYSTEM_PROMPT = """You are a helpful business analyst.
Given a SQL query, the original question, and the query results, write a clear 2-3 sentence plain-English summary.
Be specific — mention actual numbers, names, or values from the results.
Keep it concise and business-friendly."""

def summarize_results(question: str, sql: str, df: pd.DataFrame) -> str:
    if df is None or df.empty:
        return "The query returned no results."
    
    # Limit data sent to LLM to avoid token bloat
    preview = df.head(10).to_string(index=False)
    row_count = len(df)
    
    user_message = f"""Question: {question}

SQL Query Used:
{sql}

Query Results ({row_count} rows total, showing up to 10):
{preview}

Write a 2-3 sentence business summary of these results:"""
    
    return call_llm(SYSTEM_PROMPT, user_message, max_tokens=300)