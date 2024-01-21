import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

def create_quiz(genre="Python", num_questions=3, num_options=4):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            # {"role": "system", "content": "You are a helpful assistant. You can create a quiz about anything."},
            # {"role": "user", "content": f"I want {num_questions} questions with {num_options} answer options about {genre}."}
            {"role": "system", "content": "あなたは優秀なアシスタントです。あなたはあらゆるジャンルのクイズを作ることが出来ます。日本語で回答してください。lang:ja"},
            {"role": "user", "content": f"ジャンル「{genre}」に関するクイズを、{num_questions}問作ってください。{num_options}択クイズでお願いします."}
        ],
        tools = [{
            "type": "function",
            "function": {
                "name": "create_questions",
                "description": "Get quiz for given genre",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "questions": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "question": {
                                        "type": "string",
                                        "description": "Question to ask"
                                    },
                                    "options": {
                                        "type": "array",
                                        "items": {
                                            "type": "string"
                                        },
                                        "description": "Options to choose from"
                                    },
                                    "answerIndex": {
                                        "type": "number",
                                        "description": "Index of the correct answer in the options array"
                                    }
                                },
                            },
                        },
                    },
                    "required": [
                        "questions",
                    ]
                }
            }
        }],
        tool_choice={"type": "function", "function": {"name": "create_questions"}},
    )
    message = response.choices[0].message
    args = json.loads(message.tool_calls[0].function.arguments)
    return args["questions"]

if __name__ == "__main__":
    print(create_quiz())