import unittest
from unittest.mock import patch

from chatbot.agent.Agent import Agent
from chatbot.service.BotService import BotService


class TestAgent(unittest.TestCase):

    def setUp(self):
        self.agent = Agent()
        self.client = self.agent.app.test_client()
        self.client.testing = True

    @patch.object(BotService, 'prompt_and_respond')
    def test_prompt_success(self, mock_prompt_and_respond):
        # Mock the response from BotService
        mock_prompt_and_respond.return_value = "The house at 123 Main Street has 3 bedrooms."

        # Sending a request with a valid question
        response = self.client.post('/prompt',
                                    json={'question': "How many rooms does the house at 123 Main Street have?"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "The house at 123 Main Street has 3 bedrooms.")

    def test_prompt_bad_request(self):
        # Sending a request without a question
        response = self.client.post('/prompt', json={})

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Question is required", response.data)
