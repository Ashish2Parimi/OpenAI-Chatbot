import unittest
from unittest.mock import patch, Mock

import openai
from flask import Flask

from chatbot.accessor.OpenAIAccessor import OpenAIAccessor
from chatbot.exceptions.InternalServiceException import InternalServiceException


class TestOpenAIAccessor(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.context = self.app.app_context()
        self.context.push()
        env_vars = {
            'OPENAI_API_KEY': 'api_key',
            'OPENAI_MODEL': 'model',
            'OPENAI_TONE': 'tone',
            'OPENAI_TEMPERATURE': '0.5',
            'OPENAI_MAX_TOKENS': '100'
        }
        patcher = patch.dict('os.environ', env_vars)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.openai_accessor = OpenAIAccessor()

    @patch('openai.ChatCompletion.create')
    def test_get_response_success(self, mock_create):
        mock_choice = Mock()
        mock_choice.message.content = 'response_content'
        mock_create.return_value.choices = [mock_choice]

        context = "context"
        question = "question"
        response, status_code = self.openai_accessor.get_response(context, question)

        self.assertEqual(response.json, {"response": 'response_content'})
        self.assertEqual(status_code, 200)

    @patch('openai.ChatCompletion.create')
    def test_get_response_openai_error(self, mock_create):
        mock_create.side_effect = openai.error.OpenAIError('An error occurred')

        context = "context"
        question = "question"

        with self.assertRaises(InternalServiceException):
            self.openai_accessor.get_response(context, question)
