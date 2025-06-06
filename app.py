import streamlit as st
import google.generativeai as genai
import sqlite3

# Configure the Gemini API
try:
    # Use Streamlit's secrets management
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"]) 
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}")
    st.stop()

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config)

st.title("🇫🇷 Your Personal French Tutor AI")

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

st.header("Add a New Word")

with st.form("new_word_form"):
    french_word = st.text_input("Enter a French word:")
    submitted = st.form_submit_button("Add Word")

    if submitted and french_word:
        with st.spinner("Getting information..."):
            # Use Gemini to get the translation and an example
            prompt_parts = [
                f"Give me the English translation and a simple example sentence for the French word: '{french_word}'."
            ]
            response = model.generate_content(prompt_parts)

            # You'll need to parse the response from Gemini
            # This is a simplified example. You might need more robust parsing.
            try:
                # A more robust approach would be to ask Gemini for a JSON response
                lines = response.text.strip().split('\n')
                translation = lines[0].split(':')[1].strip()
                example = lines[1].split(':')[1].strip()

                # Add to the database
                conn = sqlite3.connect('vocabulary.db')
                c = conn.cursor()
                c.execute("INSERT INTO vocabulary (french_word, english_translation, example_sentence) VALUES (?, ?, ?)",
                          (french_word, translation, example))
                conn.commit()
                conn.close()

                st.success(f"Added '{french_word}' to your vocabulary!")
                st.write(f"**Translation:** {translation}")
                st.write(f"**Example:** {example}")

            except Exception as e:
                st.error(f"Could not parse the response from the AI. Please try again. Error: {e}")


# --- quiz section ---

st.header("Quiz Yourself!")

# Function to get words for the quiz
def get_quiz_words():
    conn = sqlite3.connect('vocabulary.db')
    c = conn.cursor()
    c.execute("SELECT french_word, english_translation FROM vocabulary ORDER BY RANDOM() LIMIT 5")
    words = c.fetchall()
    conn.close()
    return words

if 'quiz_words' not in st.session_state:
    st.session_state.quiz_words = []
    st.session_state.current_question = 0
    st.session_state.score = 0

if st.button("Start Quiz"):
    st.session_state.quiz_words = get_quiz_words()
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.experimental_rerun()

if st.session_state.quiz_words:
    if st.session_state.current_question < len(st.session_state.quiz_words):
        word_pair = st.session_state.quiz_words[st.session_state.current_question]
        french_word, correct_translation = word_pair

        st.write(f"What is the English translation of: **{french_word}**?")

        user_answer = st.text_input("Your Answer:", key=f"q_{st.session_state.current_question}")

        if st.button("Submit Answer"):
            if user_answer.strip().lower() == correct_translation.lower():
                st.success("Correct! 🎉")
                st.session_state.score += 1
            else:
                st.error(f"Sorry, the correct answer is: **{correct_translation}**")

            st.session_state.current_question += 1
            st.experimental_rerun()

    else:
        st.write(f"Quiz finished! Your score is: {st.session_state.score}/{len(st.session_state.quiz_words)}")
        st.session_state.quiz_words = [] # Reset the quiz