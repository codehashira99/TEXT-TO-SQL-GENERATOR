import sqlite3
import os

def init_database():
    db_path = os.path.join(os.path.dirname(__file__), "sample.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r") as f:
        cursor.executescript(f.read())
    
    seed_path = os.path.join(os.path.dirname(__file__), "seed_data.sql")
    with open(seed_path, "r") as f:
        cursor.executescript(f.read())
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized at: {db_path}")

if __name__ == "__main__":
    init_database()