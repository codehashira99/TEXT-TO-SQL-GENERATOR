import re

BLOCKED_KEYWORDS = [
    r'\bDROP\b', r'\bDELETE\b', r'\bUPDATE\b', r'\bINSERT\b',
    r'\bALTER\b', r'\bCREATE\b', r'\bTRUNCATE\b', r'\bREPLACE\b',
    r'\bEXEC\b', r'\bEXECUTE\b', r'\bATTACH\b', r'\bDETACH\b',
    r'\bPRAGMA\b', r'--', r'/\*'
]

def validate_sql(sql: str) -> tuple[bool, str]:
    """
    Returns (is_safe, error_message).
    is_safe=True means query is safe to run.
    """
    if not sql or not sql.strip():
        return False, "Empty query generated."
    
    sql_upper = sql.upper()
    
    # Must start with SELECT
    if not sql_upper.strip().startswith("SELECT"):
        return False, f"Only SELECT queries are allowed. Got: {sql[:50]}..."
    
    # Check for blocked keywords
    for pattern in BLOCKED_KEYWORDS:
        if re.search(pattern, sql_upper):
            keyword = pattern.replace(r'\b', '').replace('\\', '')
            return False, f"Blocked keyword detected: {keyword}"
    
    # Block multiple statements
    statements = [s.strip() for s in sql.split(';') if s.strip()]
    if len(statements) > 1:
        return False, "Multiple SQL statements are not allowed."
    
    return True, ""