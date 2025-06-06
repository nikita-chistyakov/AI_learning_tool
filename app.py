# app.py
import streamlit as st
from src.gemini_service import configure_gemini, get_word_info_from_ai, get_ai_response_for_qa
from src.database_manager import init_db, add_vocabulary_entry, get_all_vocabulary, get_quiz_words
from src.quiz_logic import QuizManager # Consider a class for quiz state
from src.utils import display_word_details # Example utility

# Configure Gemini API (this needs to be in app.py or called very early)
try:
    # This will load from .streamlit/secrets.toml locally or Streamlit Cloud secrets
    configure_gemini(st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}")
    st.stop()

# Initialize the database (this will run once when the app starts)
init_db()

st.title("Language learning with AI")

# --- LLM for Q&A Section ---
st.header("Ask your new French tutor")
user_question = st.text_area("Ask me anything about French language or learning!")

if st.button("Get Answer / Répondre"):
    if user_question:
        with st.spinner("Thinking..."):
            try:
                ai_answer = get_ai_response_for_qa(user_question)
                st.markdown(ai_answer)
            except Exception as e:
                st.error(f"Error getting AI answer: {e}")
    else:
        st.warning("Please enter a question.")

# --- Initialize Session State (Crucial for Streamlit) ---
if 'quiz_manager' not in st.session_state:
    st.session_state.quiz_manager = QuizManager() # Initialize your quiz manager object

# --- Add Word Section ---
st.header("Add a New Word (FR: ajouter un nouveau mot)")
with st.form("new_word_form"):
    french_word_input = st.text_input("Enter a French word:")
    submitted = st.form_submit_button("Add Word / Ajouter un mot")

    if submitted and french_word_input:
        with st.spinner(f"Getting translation and example for '{french_word_input}'..."):
            try:
                word_data = get_word_info_from_ai(french_word_input)
                if word_data:
                    add_vocabulary_entry(
                        word_data["french_word"],
                        word_data["english_translation"],
                        word_data["example_sentence"]
                    )
                    st.success(f"Added '{word_data['french_word']}' to your vocabulary!")
                    display_word_details(word_data)
                else:
                    st.error("AI did not provide complete information. Please try again.")
            except Exception as e:
                st.error(f"Error processing word: {e}")

# --- Display Vocabulary Section ---
st.header("Your Vocabulary")
vocabulary_list = get_all_vocabulary()
if vocabulary_list:
    for word in vocabulary_list:
        with st.expander(f"**{word[0]}** - {word[1]}"): # french, english
            st.write(f"**Example:** {word[2]}") # example_sentence
else:
    st.info("Your vocabulary list is empty. Add some words above!")


# --- Quiz Section ---
st.header("Quiz Yourself!")
st.session_state.quiz_manager.display_quiz_ui() # Delegate UI to QuizManager
