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
        st.session_state.user_answers = []  # Initialize user_answers in session_state

# Display question and options
def display_question(question):
    st.write(question['question'])
    return st.radio("Choose one:", question['options'], key='radio')

# Check answer and update state
def check_answer(answer, question):
    if st.button('Submit', key='submit_button'):
        correct = answer == question['options'][question['answerIndex']]
        if correct:
            st.session_state.score += 1
            st.session_state.message = 'Correct!'
        else:
            st.session_state.message = f'Incorrect. The correct answer is {question["options"][question["answerIndex"]]}.'
        st.session_state.show_next = True
        st.session_state.user_answers.append((question['question'], answer, correct, question['options'][question['answerIndex']]))  # Save user's answer and its correctness
        st.experimental_rerun()

# Move to next question
def next_question():
    if st.button('Next Question', key='next_button'):
        st.session_state.quiz_state += 1
        st.session_state.show_next = False
        st.session_state.message = ""
        st.experimental_rerun()

# Display final score and answers
def display_final_score_and_answers():
    st.write('Your final score is:', st.session_state.score)
    for question, user_answer, correct, correct_answer in st.session_state.user_answers:
        st.write(f"Question: {question}")
        st.write(f"Your answer: {user_answer} ({'Correct' if correct else 'Incorrect'})")
        st.write(f"Correct answer: {correct_answer}")
        st.write("---")

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
        display_final_score_and_answers()

# Run quiz
questions = load_questions(QUESTIONS_FILE)
quiz(questions)