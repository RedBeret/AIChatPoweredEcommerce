import os

import openai
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

app = Flask(__name__)

TEMP_USER_ID = 1


@app.route("/chat_messages", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    thread_id = data.get("thread_id")

    if not thread_id:
        thread_response = client.threads.create()
        thread_id = thread_response.id

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ],
        thread_id=thread_id,
        temperature=0.7,
        max_tokens=150,
    )

    ai_response = response.choices[0].message.content.strip()
    return jsonify({"response": ai_response, "thread_id": thread_id})


def add_message_and_get_response(thread_id, user_message):
    message_response = openai.Message.create(
        thread_id=thread_id, role="user", content=user_message
    )

    run_response = openai.Run.create(
        thread_id=thread_id,
        assistant_id="your-assistant-id",
    )

    ai_response = run_response.choices[0].message.content
    return ai_response


def get_completion(
    prompt, model="gpt-4", temperature=0.7, max_tokens=150, thread_id=None
):
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
            thread_id=thread_id,
        )
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content.strip(), thread_id
    except Exception as e:
        print(f"Error: {e}")
    return None, thread_id


def main():
    thread_id = None

    while True:
        prompt = input("Enter prompt (or type 'exit' to quit): ")
        if prompt.lower() == "exit":
            print("Exiting...")
            break

        if not thread_id:
            thread_response = client.threads.create()
            thread_id = thread_response.id
            print(f"New thread created with ID: {thread_id}")

        response, thread_id = get_completion(prompt, thread_id=thread_id)
        print("Response:", response)


if __name__ == "__main__":
    main()
