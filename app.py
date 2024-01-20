import streamlit as st
import json

# Load questions
with open('data/questions.json', 'r') as f:
    questions = json.load(f)

# Quiz logic
def quiz(questions):
    score = 0
    for i, question in enumerate(questions):
        st.write(question['question'])
        answer = st.selectbox("Choose one:", question['options'], key=i)
        if st.button('Submit', key=f"button{i}"):
            if answer == question['answer']:
                score += 1
                st.write('Correct!')
            else:
                st.write('Incorrect.')
    st.write('Your final score is:', score)

# Run quiz
quiz(questions)