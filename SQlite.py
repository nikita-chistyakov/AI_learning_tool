import sqlite3

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('vocabulary.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS vocabulary (
            id INTEGER PRIMARY KEY,
            french_word TEXT NOT NULL,
            english_translation TEXT NOT NULL,
            example_sentence TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()