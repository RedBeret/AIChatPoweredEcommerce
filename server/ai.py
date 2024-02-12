"""
OpenAI API CLI Testing Tool

I created this to test my connection then I integrated it into my app.py but wanted to leave
as it may be helpful if anyone wanted to use it and test it. This script provides a command-line 
interface (CLI) for interacting with the OpenAI API, allowing users to test the natural language 
processing capabilities of OpenAI's models. It's designed for developers and enthusiasts 
who wish to explore the power of AI for generating text completions, answering questions, 
or any other task that OpenAI's models are trained on.

Usage:
1. Ensure you have an OpenAI API key. If not, obtain one by signing up at https://openai.com/.
2. Store your API key in a .env file in the same directory as this script with the following content:
   OPENAI_API_KEY='your_api_key_here'
3. Run this script from the command line. You will be prompted to enter text, and the AI's response
   will be displayed in the console.
4. Type 'exit' to quit the tool at any time.

Prerequisites:
- Python 3
- openai Python package (install with 'pip install openai')
- dotenv Python package (install with 'pip install python-dotenv')

This tool is intended for educational and testing purposes, providing a quick and easy way
to interact with the OpenAI API without the need for setting up a full application.
"""

import os

import openai
from dotenv import load_dotenv
from flask import Flask

# Load environment variables from the .env file for secure API key management
load_dotenv()

# Initialize OpenAI client with API key from environment variables
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Retrieve the OpenAI API key and Assistant ID from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")

# Initialize Flask app (for potential future web server extension)
app = Flask(__name__)

# Temporary user ID for CLI session management
TEMP_USER_ID = 1

# Assistant ID for OpenAI chat completion (replace with your Assistant's ID)
assistant_id = OPENAI_ASSISTANT_ID

# Reinitialize OpenAI client (if needed) and Flask app
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
app = Flask(__name__)


# also if you want to change the models change the content where it has you are a helpful assistant
# to what you may want like you are a math tutor or what you want it to act like.
def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.7, max_tokens=150):
    """
    Generates a response from OpenAI based on the provided prompt.
    Uses a fixed system role message for initialization and user's input as prompt.

    :param prompt: User's input to generate a response for.
    :param model: The model used for generating completions.
    :param temperature: Controls randomness in the response generation.
    :param max_tokens: The maximum number of tokens in the generated response.
    :return: The generated response from OpenAI or None in case of an error.
    """
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
        return response.choices[0].message.content.strip() if response.choices else None
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    """
    Main function to run the CLI tool.
    """
    print("OpenAI API Test CLI")
    print("Type 'exit' to quit at any time.")

    while True:
        prompt = input("Enter prompt: ")
        if prompt.lower() == "exit":
            print("Exiting...")
            break

        response = get_completion(prompt)
        print("AI Response:", response)


if __name__ == "__main__":
    main()
