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
             "content": os.environ.get('OPENAI_TONE')},  # this is the tone of the chatbot's response
            {"role": "user", "content": context},
            {"role": "user", "content": question}
        ]

        try:
            chat_completion = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=float(os.environ.get('OPENAI_TEMPERATURE')),  # degree of randomness of the model's output
                max_tokens=int(os.environ.get('OPENAI_MAX_TOKENS')),  # the maximum number of tokens to generate
            )

        except openai.error.OpenAIError as e:
            app.logging.error(f"OpenAI API error: {e}")
            raise InternalServiceException(f"OpenAI API error: {e}")

        return jsonify({"response": chat_completion.choices[0].message.content}), 200
