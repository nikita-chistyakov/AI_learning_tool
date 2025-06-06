# src/database_manager.py
import sqlite3
import streamlit as st

DATABASE_FILE = 'vocabulary.db'

@st.cache_resource
def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
    # IMPORTANT: Do NOT close the connection here when using @st.cache_resource
    return conn

def init_db():
    conn = get_db_connection()
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
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO vocabulary (french_word, english_translation, example_sentence) VALUES (?, ?, ?)",
              (french_word, english_translation, example_sentence))
    conn.commit()
    # REMOVED: conn.close()

def get_all_vocabulary() -> list[tuple]:
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT french_word, english_translation, example_sentence FROM vocabulary")
    words = c.fetchall()
    # REMOVED: conn.close()
    return words

def get_quiz_words(limit: int = 5) -> list[tuple]:
    conn = get_db_connection() # This gets the cached, persistent connection
    c = conn.cursor()
    c.execute(f"SELECT french_word, english_translation FROM vocabulary ORDER BY RANDOM() LIMIT {limit}")
    words = c.fetchall()
    # <<<<<<<<< Make sure this line is GONE: conn.close() >>>>>>>>>>
    return words