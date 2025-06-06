# src/quiz_logic.py
import streamlit as st
from src.database_manager import get_quiz_words

class QuizManager:
    def __init__(self):
        # Initialize quiz state if not already in session_state
        if 'quiz_words' not in st.session_state:
            st.session_state.quiz_words = []
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.quiz_started = False
            st.session_state.last_answer_correct = None

    def start_quiz(self):
        """Starts a new quiz."""
        all_words = get_quiz_words(limit=5) # Get 5 random words
        if all_words:
            st.session_state.quiz_words = all_words
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.quiz_started = True
            st.session_state.last_answer_correct = None
            st.rerun()
        else:
            st.warning("Please add some words to your vocabulary before starting a quiz.")

    def check_answer(self, user_answer: str):
        """Checks the user's answer and updates score."""
        if st.session_state.current_question < len(st.session_state.quiz_words):
            _, correct_translation = st.session_state.quiz_words[st.session_state.current_question]
            if user_answer.strip().lower() == correct_translation.lower():
                st.session_state.last_answer_correct = True
                st.session_state.score += 1
            else:
                st.session_state.last_answer_correct = False
            st.rerun() # Rerun to show feedback

    def next_question(self):
        """Moves to the next question in the quiz."""
        st.session_state.current_question += 1
        st.session_state.last_answer_correct = None # Reset feedback for next question
        st.rerun() # Rerun to display next question or results

    def reset_quiz(self):
        """Resets all quiz-related session state variables."""
        st.session_state.quiz_words = []
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.quiz_started = False
        st.session_state.last_answer_correct = None
        st.rerun()

    def display_quiz_ui(self):
        """Displays the quiz UI based on the current state."""
        if not st.session_state.quiz_started:
            if st.button("Start Quiz"):
                self.start_quiz()
        else:
            if st.session_state.current_question < len(st.session_state.quiz_words):
                french_word, correct_translation = st.session_state.quiz_words[st.session_state.current_question]
                st.markdown(f"### Question {st.session_state.current_question + 1}/{len(st.session_state.quiz_words)}")
                st.write(f"What is the English translation of: **{french_word}**?")

                user_answer = st.text_input("Your Answer:", key=f"q_{st.session_state.current_question}")

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Check Answer", disabled=st.session_state.last_answer_correct is not None):
                        self.check_answer(user_answer)

                if st.session_state.last_answer_correct is not None:
                    if st.session_state.last_answer_correct:
                        st.success("Correct! 🎉")
                    else:
                        st.error(f"Sorry, the correct answer is: **{correct_translation}**")

                    with col2:
                        if st.button("Next Question", disabled=st.session_state.last_answer_correct is None):
                            self.next_question()
            else:
                st.markdown("---")
                st.success(f"Quiz finished! Your final score is: **{st.session_state.score}/{len(st.session_state.quiz_words)}**")
                if st.button("Restart Quiz"):
                    self.reset_quiz()