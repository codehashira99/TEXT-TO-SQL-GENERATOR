import json
import re
import os
from core.llm_client import call_llm

def load_schema() -> str:
    schema_path = os.path.join("schema", "schema_description.json")
    with open(schema_path, "r") as f:
        schema = json.load(f)
    
    lines = [f"Database: {schema['database']}\n"]
    for table, info in schema["tables"].items():
        lines.append(f"Table: {table} — {info['description']}")
        for col, desc in info["columns"].items():
            lines.append(f"  - {col}: {desc}")
        lines.append("")
    lines.append("Relationships:")
    for rel in schema["relationships"]:
        lines.append(f"  {rel}")
    return "\n".join(lines)

SYSTEM_PROMPT = """You are an expert SQL generator for SQLite databases.
Given a database schema and a natural language question, generate a valid SQLite SELECT query.

Rules:
- Only generate SELECT statements. Never use DROP, DELETE, UPDATE, INSERT, ALTER, CREATE.
- Use proper JOINs when needed based on relationships.
- Use table aliases for clarity.
- Return ONLY the SQL query, nothing else — no explanations, no markdown, no backticks.
- If the question cannot be answered with the schema, return: SELECT 'Unable to answer with available data' as message;
"""

def generate_sql(natural_language_query: str) -> str:
    schema_text = load_schema()
    user_message = f"""Schema:
{schema_text}

Question: {natural_language_query}

Generate the SQLite SELECT query:"""
    
    raw_response = call_llm(SYSTEM_PROMPT, user_message)
    
    # Clean up response — strip markdown fences if LLM adds them
    sql = raw_response.strip()
    sql = re.sub(r"^```sql\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"^```\s*", "", sql)
    sql = re.sub(r"\s*```$", "", sql)
    return sql.strip()