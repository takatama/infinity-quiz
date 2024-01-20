import streamlit as st
import json

# Load questions
with open('data/questions.json', 'r') as f:
    questions = json.load(f)

# Quiz logic
def quiz(questions):
    if 'quiz_state' not in st.session_state:
        st.session_state.quiz_state = 0  # Initialize quiz_state in session_state
        st.session_state.score = 0  # Initialize score in session_state
        st.session_state.show_next = False  # Initialize show_next in session_state
        st.session_state.message = ""  # Initialize message in session_state

    if st.session_state.quiz_state < len(questions):
        question = questions[st.session_state.quiz_state]
        st.write(question['question'])
        answer = st.selectbox("Choose one:", question['options'], key='selectbox')

        if st.session_state.show_next:
            st.write(st.session_state.message)  # Display the message
            if st.button('Next Question', key='next_button'):
                st.session_state.quiz_state += 1  # Move to next question
                st.session_state.show_next = False  # Reset show_next flag
                st.session_state.message = ""  # Reset the message
                st.experimental_rerun()  # Rerun the script to update the state
        else:
            if st.button('Submit', key='submit_button'):
                if answer == question['answer']:
                    st.session_state.score += 1
                    st.session_state.message = 'Correct!'  # Set the message
                else:
                    st.session_state.message = 'Incorrect.'  # Set the message
                st.session_state.show_next = True  # Set show_next flag to True
                st.experimental_rerun()  # Rerun the script to update the state
    else:
        st.write('Your final score is:', st.session_state.score)

# Run quiz
quiz(questions)