# Text-to-SQL AI

Query your business database using plain English — powered by Claude.

## Setup

1. Install dependencies:
```bash
   pip install -r requirements.txt
```

2. Set your API key:
```bash
   export ANTHROPIC_API_KEY=your_key_here
```

3. Initialize the database:
```bash
   python database/init_db.py
```

4. Run the app:
```bash
   streamlit run app.py
```

## Sample Queries
- "What are the top 5 customers by total order value?"
- "Show all completed orders in 2024"
- "Average product price by category"
- "Which products have low stock?"
- "Monthly revenue trend"

## Safety
- Only SELECT queries are allowed
- Blocks: DROP, DELETE, UPDATE, INSERT, ALTER, TRUNCATE, PRAGMA
- Multiple statement execution is blocked