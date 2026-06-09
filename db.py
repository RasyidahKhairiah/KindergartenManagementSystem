import sqlite3

def create_db():
    conn = sqlite3.connect('userid.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        email TEXT,
        password TEXT,
        role TEXT
    )''')
    conn.commit()
    conn.close()

create_db()