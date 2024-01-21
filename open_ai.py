import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def create_quiz(genre="Python", num_questions=3, num_options=4):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You can create a quiz about anything. 日本語で回答してください。lang:ja"},
            {"role": "user", "content": f"I want {num_questions} questions with {num_options} answer options about {genre}."}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print(create_quiz())