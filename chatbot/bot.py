import json
import logging
import sqlite3

import openai
from flask import Flask, jsonify, request

from chatbot.config import Config


class PropertyBot:

    def __init__(self):
        self.app = Flask(__name__)
        openai.api_key = Config.OPENAI_API_KEY
        self.app.add_url_rule('/ask', view_func=ask, methods=['POST'])

    def run(self):
        self.app.run(debug=True)


def ask():
    """
    This function is called when the user sends a POST request to the /ask endpoint.
    It expects a JSON object with a question field. It returns a JSON object with a response field.
    """
    question = request.json.get('question')

    if not question:
        logging.error("Bad Request: Question is required")
        return jsonify({"error": "Bad Request: Question is required"}), 400

    description = get_description_from_db(question)

    messages = [
        {"role": "system", "content": "You are a helpful property agent who answers questions based on given content "
                                      "and question. The content can be  description of property or an error message. "
                                      "if its error please ask the user to try after sometime proving a simple "
                                      "response of whats the issue"},
        {"role": "user", "content": description},
        {"role": "user", "content": question}
    ]

    try:
        chat_completion = openai.ChatCompletion.create(
            model=Config.OPENAI_MODEL,
            messages=messages
        )

    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return jsonify({"error": f"OpenAI API error: {e}"}), 500

    return jsonify({"response": chat_completion.choices[0].message.content}), 200


def get_description_from_db(question):
    address = extract_address(question)
    if not address:
        return "description: We don't have the info about this address"
    try:
        with sqlite3.connect(Config.DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT description FROM properties WHERE address = ?", (address,))
            return "description: " + c.fetchone()[0]
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return f"Database error: {e}"


def extract_address(question):
    # Logic to extract the address from the question
    with open('./data.json', 'r') as file:
        properties = json.load(file)
    keys = properties.keys()
    for address_key in keys:
        if address_key in question:
            return address_key
    return None


if __name__ == '__main__':
    bot = PropertyBot()
    bot.run()
