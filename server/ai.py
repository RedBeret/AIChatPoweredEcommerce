import os

import openai
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, jsonify, request
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")

app = Flask(__name__)

TEMP_USER_ID = 1


assistant_id = OPENAI_ASSISTANT_ID

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

app = Flask(__name__)


def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.7, max_tokens=150):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
    return None


def main():
    # Start Flask app
    app.run(port=5555, debug=True, use_reloader=False)

    # CLI testing
    thread_id = None

    while True:
        prompt = input("Enter prompt (or type 'exit' to quit): ")
        if prompt.lower() == "exit":
            print("Exiting...")
            break

        if not thread_id:

            pass

        response = get_completion(prompt)
        print("Response:", response)


if __name__ == "__main__":
    main()
