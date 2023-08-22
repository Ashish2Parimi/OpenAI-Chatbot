import logging

from flask import Flask, request

from chatbot.exceptions.BadRequest import BadRequest
from chatbot.service.BotService import BotService


class Agent:
    """
    This is a chatbot of a helpful property agent who answers questions based on given content and question.
    ---
    parameters:
        - name: question
            in: body
            type: string
            required: true
            default: "How many rooms does the house at 123 Main Street have?"
            description: The question asked by the user

    responses:
        200:
            description: The response from the bot answering the question
        400:
            description: Bad Request - Question is required
        500:
            description: Internal Server Error - Unable to reach database, OpenAI API, or other internal error
    examples:
        How many rooms does the house at 123 Main Street have? : The house at 123 Main Street has 3 bedrooms.

    """

    def __init__(self):
        self.app = Flask(__name__)
        self.service = BotService()
        self.app.add_url_rule('/prompt', view_func=self.prompt, methods=['POST'])

    def prompt(self):
        question = request.json.get('question')

        if not question:
            logging.error("Bad Request: Question is required")
            raise BadRequest("Question is required")

        return self.service.prompt_and_respond(question)


if __name__ == '__main__':
    app = Agent().app
    app.run(debug=True)
