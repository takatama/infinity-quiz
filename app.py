import streamlit as st
import json

# Load questions
with open('data/questions.json', 'r') as f:
    questions = json.load(f)

# Quiz logic
def quiz(questions):
    score = 0
    for question in questions:
        st.write(question['question'])
        answer = st.selectbox("Choose one:", question['options'])
        if st.button('Submit'):
            if answer == question['answer']:
                score += 1
                st.write('Correct!')
            else:
                st.write('Incorrect.')
    st.write('Your final score is:', score)

# Run quiz
quiz(questions)