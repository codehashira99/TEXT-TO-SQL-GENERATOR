# Text-to-SQL AI

WHAT IS THE NEED OF THIS TOOL?
Non-technical stakeholders (sales managers, marketing teams, product owners) frequently need ad-hoc insights from business databases but lack SQL expertise, creating dependency on data analysts and causing delays in decision-making. Build an AI-powered tool that allows users to query a database using natural language, automatically converting questions into SQL, executing them safely, and returning both raw results and a plain-English summary — eliminating the SQL knowledge barrier for data access.

I have added project demo -- screencast file, that shows working of project.

Query your business database using plain English 

## Setup

1. Install dependencies:
```bash
   pip install -r requirements.txt
```

2. Set your API key:
```bash
   export GROQ_API_KEY=gsk_yourkey
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
