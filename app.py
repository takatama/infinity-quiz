import streamlit as st
import json

# Constants
QUESTIONS_FILE = 'data/questions.json'

# Load questions
def load_questions(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Initialize session state
def initialize_state():
    if 'quiz_state' not in st.session_state:
        st.session_state.quiz_state = 0
        st.session_state.score = 0
        st.session_state.show_next = False
        st.session_state.message = ""

# Display question and options
def display_question(question):
    st.write(question['question'])
    return st.selectbox("Choose one:", question['options'], key='selectbox')

# Check answer and update state
def check_answer(answer, question):
    if st.button('Submit', key='submit_button'):
        if answer == question['answer']:
            st.session_state.score += 1
            st.session_state.message = 'Correct!'
        else:
            st.session_state.message = 'Incorrect.'
        st.session_state.show_next = True
        st.experimental_rerun()

# Move to next question
def next_question():
    if st.button('Next Question', key='next_button'):
        st.session_state.quiz_state += 1
        st.session_state.show_next = False
        st.session_state.message = ""
        st.experimental_rerun()

# Quiz logic
def quiz(questions):
    initialize_state()

    if st.session_state.quiz_state < len(questions):
        question = questions[st.session_state.quiz_state]
        answer = display_question(question)

        if st.session_state.show_next:
            st.write(st.session_state.message)
            next_question()
        else:
            check_answer(answer, question)
    else:
        st.write('Your final score is:', st.session_state.score)

# Run quiz
questions = load_questions(QUESTIONS_FILE)
quiz(questions)