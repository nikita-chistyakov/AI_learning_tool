# src/database_manager.py
import sqlite3
import streamlit as st

DATABASE_FILE = 'vocabulary.db' # Name of your database file

# Use st.connection for persistent SQLite on Streamlit Cloud
@st.cache_resource # This caches the connection object
def get_db_connection():
    """
    Establishes and caches a SQLite database connection.
    This helps persist data on Streamlit Cloud.
    check_same_thread=False is important for Streamlit's threading model.
    """
    conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
    # Important: Do NOT close the connection here or in other functions
    # when using @st.cache_resource. Streamlit manages its lifecycle.
    return conn

def init_db():
    """Initializes the vocabulary database table if it doesn't exist."""
    conn = get_db_connection() # Get the cached connection
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
    # No conn.close() here either, as it's the cached connection

def add_vocabulary_entry(french_word: str, english_translation: str, example_sentence: str):
    """Adds a new word, translation, and example to the database."""
    conn = get_db_connection() # Get the cached connection
    c = conn.cursor()
    c.execute("INSERT INTO vocabulary (french_word, english_translation, example_sentence) VALUES (?, ?, ?)",
              (french_word, english_translation, example_sentence))
    conn.commit()
    # REMOVED: conn.close()

def get_all_vocabulary() -> list[tuple]:
    """Retrieves all vocabulary entries from the database."""
    conn = get_db_connection() # Get the cached connection
    c = conn.cursor()
    c.execute("SELECT french_word, english_translation, example_sentence FROM vocabulary")
    words = c.fetchall()
    # REMOVED: conn.close()
    return words

def get_quiz_words(limit: int = 5) -> list[tuple]:
    """Retrieves a random set of words for a quiz."""
    conn = get_db_connection() # Get the cached connection
    c = conn.cursor()
    c.execute(f"SELECT french_word, english_translation FROM vocabulary ORDER BY RANDOM() LIMIT {limit}")
    words = c.fetchall()
    # REMOVED: conn.close()
    return words