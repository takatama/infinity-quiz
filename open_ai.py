import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()


def _create_quiz_by_json_mode(client, genre, num_questions, num_options):
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            # {"role": "system", "content": "You are a helpful assistant. You can create a quiz about anything."},
            # {"role": "user", "content": f"I want {num_questions} questions with {num_options} answer options about {genre}."}
            {
                "role": "system",
                "content": 'あなたは優秀なアシスタントです。あなたはあらゆるジャンルのクイズを作ることが出来ます。日本語で回答してください。lang:ja。{"questions: [{"question": "問題", "options":["回答1", "回答2", "回答3", "回答4"], "answerIndex": 0},...]}のJSON形式で返却してください。',
            },
            {
                "role": "user",
                "content": f"ジャンル「{genre}」に関するクイズを、{num_questions}問作ってください。{num_options}択クイズでお願いします.",
            },
        ],
        response_format={"type": "json_object"},
    )
    json_obj = json.loads(response.choices[0].message.content)
    print(json_obj)
    return json_obj["questions"]


def _create_quiz_by_function_calling(client, genre, num_questions, num_options):
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            # {"role": "system", "content": "You are a helpful assistant. You can create a quiz about anything."},
            # {"role": "user", "content": f"I want {num_questions} questions with {num_options} answer options about {genre}."}
            {
                "role": "system",
                "content": "あなたは優秀なアシスタントです。あなたはあらゆるジャンルのクイズを作ることが出来ます。日本語で回答してください。lang:ja。",
            },
            {
                "role": "user",
                "content": f"ジャンル「{genre}」に関するクイズを、{num_questions}問作ってください。{num_options}択クイズでお願いします.",
            },
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "create_questions",
                    "description": "Get quiz for given genre",
                    "parameters": {
                        "$schema": "http://json-schema.org/draft-07/schema#",
                        "type": "object",
                        "properties": {
                            "questions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "question": {"type": "string"},
                                        "options": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                        },
                                        "answerIndex": {
                                            "type": "integer",
                                            "minimum": 0,
                                        },
                                    },
                                    "required": ["question", "options", "answerIndex"],
                                    "additionalProperties": False,
                                },
                            }
                        },
                        "required": ["questions"],
                        "additionalProperties": False,
                    },
                },
            }
        ],
        tool_choice={"type": "function", "function": {"name": "create_questions"}},
    )
    message = response.choices[0].message
    args = json.loads(message.tool_calls[0].function.arguments)
    print(args)
    return args["questions"]


def create_quiz(genre="Python", num_questions=3, num_options=4):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return _create_quiz_by_function_calling(client, genre, num_questions, num_options)
    # return _create_quiz_by_json_mode(client, genre, num_questions, num_options)


if __name__ == "__main__":
    print(create_quiz())
