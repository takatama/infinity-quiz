import streamlit as st
import json
from open_ai import create_quiz

# Initialize session state
def initialize_state(questions):
    if 'quiz_state' not in st.session_state:
        st.session_state.questions = questions
        st.session_state.quiz_state = 0
        st.session_state.score = 0
        st.session_state.show_next = False
        st.session_state.message = ""
        st.session_state.user_answers = []  # Initialize user_answers in session_state

# Display question and options
def display_question(question):
    st.write(question['question'])
    options = question['options'] + ['None of the above'] # 該当なし
    return st.radio("Choose one:", options, key='radio')

# Check answer and update state
def check_answer(answer, question):
    if st.button('Submit', key='submit_button'):
        correct = answer == question['options'][question['answerIndex']]
        if answer == 'None of the above':
            st.session_state.message = f"I'm sorry. The answer I had in mind was {question['options'][question['answerIndex']]}."
        elif correct:
            st.session_state.score += 1
            st.session_state.message = 'Correct!'
        else:
            st.session_state.message = f'Incorrect. The correct answer is {question["options"][question["answerIndex"]]}.'
        st.session_state.show_next = True
        st.session_state.user_answers.append((question['question'], answer, correct, question['options'][question['answerIndex']]))  # Save user's answer and its correctness
        st.rerun()

# Move to next question
def next_question(questions):
    button_label = 'Show Results' if st.session_state.quiz_state == len(questions) - 1 else 'Next Question'
    if st.button(button_label, key='next_button'):
        st.session_state.quiz_state += 1
        st.session_state.show_next = False
        st.session_state.message = ""
        st.rerun()

# Display final score and answers
def display_final_score_and_answers():
    st.write('Your final score is:', st.session_state.score)
    for question, user_answer, correct, correct_answer in st.session_state.user_answers:
        st.write(f"Question: {question}")
        st.write(f"Your answer: {user_answer} ({'Correct' if correct else 'Incorrect'})")
        st.write(f"Correct answer: {correct_answer}")
        st.write("---")
    if st.button("Retry"):
        st.session_state.clear()
        st.rerun()

# Quiz logic
def quiz(questions):
    if st.session_state.quiz_state < len(questions):
        question = questions[st.session_state.quiz_state]
        answer = display_question(question)

        if st.session_state.show_next:
            st.write(st.session_state.message)
            next_question(questions)
        else:
            check_answer(answer, question)
    else:
        display_final_score_and_answers()

# Run quiz
genre = st.text_input("Enter a genre", "Python")
if (st.button("Start")):
    st.session_state.clear()
    questions = create_quiz(genre)
    print(questions)
    initialize_state(questions)

if 'questions' in st.session_state:
    quiz(st.session_state.questions)
else:
    st.write("Click 'Start' to start the quiz.")