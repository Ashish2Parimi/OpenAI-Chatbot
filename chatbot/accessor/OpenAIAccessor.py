import os
from pathlib import Path

import openai
from flask import app, jsonify
from flask.cli import load_dotenv

from chatbot.Exceptions.InternalServiceException import InternalServiceException


class OpenAIAccessor:

    def __init__(self):
        # Load the environment variables from the OpenAI_config.env file
        current_dir = Path(__file__).parent.parent
        load_dotenv(current_dir / 'config/OpenAI_config.env')
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        self.model = os.environ.get('OPENAI_MODEL')

    def get_response(self, context, question):

        messages = [
            {"role": "system",
             "content": "You are a helpful real-estate agent who answers questions based on given context "
                        "and question. The content can be  description of property or an error message. "
                        "if its error please ask the user to try after sometime proving a simple "
                        "response"},
            {"role": "user", "content": context},
            {"role": "user", "content": question}
        ]

        try:
            chat_completion = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=1,  # this is the degree of randomness of the model's output
                max_tokens=100,  # the maximum number of tokens to generate
            )

        except openai.error.OpenAIError as e:
            app.logging.error(f"OpenAI API error: {e}")
            raise InternalServiceException(f"OpenAI API error: {e}")

        return jsonify({"response": chat_completion.choices[0].message.content}), 200
