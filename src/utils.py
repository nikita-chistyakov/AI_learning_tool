# src/utils.py
import streamlit as st

def display_word_details(word_data: dict):
    """Helper to display word translation and example consistently."""
    st.write(f"**French Word:** {word_data.get('french_word')}")
    st.write(f"**Translation:** {word_data.get('english_translation')}")
    st.write(f"**Example:** {word_data.get('example_sentence')}")

# Add more utility functions here as your app grows