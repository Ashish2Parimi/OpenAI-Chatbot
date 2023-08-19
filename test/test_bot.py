import sqlite3
import unittest
from unittest.mock import patch, Mock

from chatbot.bot import PropertyBot, get_description_from_db


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app_instance = PropertyBot()
        self.app = self.app_instance.app.test_client()

    @patch("sqlite3.connect")
    def test_get_description_from_db_Success(self, mock_connect):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = ('A 3-bedroom house, the price is 568,000 dollars',)
        mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        description = get_description_from_db('123 Main Street')

        self.assertEqual(description, 'description: A 3-bedroom house, the price is 568,000 dollars')
        mock_cursor.execute.assert_called_once_with("SELECT description FROM properties WHERE address = ?",
                                                    ('123 Main Street',))

    @patch("sqlite3.connect")
    def test_get_description_from_db_error(self, mock_connect):
        # Set up the mock to raise an exception when called
        mock_connect.side_effect = sqlite3.Error("Database error")

        # Call the function
        description = get_description_from_db('123 Main Street')

        # Assert that the function handled the error correctly and returned None
        self.assertEqual(description, 'Database error: Database error')

    @patch("sqlite3.connect")
    def test_get_description_from_db_no_description_found(self, mock_connect):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = "We don't have the info about this address"
        mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        description = get_description_from_db('459 Oak Avenue')
        self.assertEqual(description, "description: We don't have the info about this address")

    @patch("sqlite3.connect")
    @patch('openai.ChatCompletion.create')
    def test_ask_Success(self, mock_openai_create, mock_connect):
        # Set the return value for OpenAI's ChatCompletion.create call
        mock_openai_create.return_value = type('', (), {
            'choices': [
                type('', (), {'message': type('', (), {'content': 'The price is 568,000 dollars'})})
            ]
        })
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = ('A 3-bedroom house, the price is 568,000 dollars',)
        mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor
        response = self.app.post('/ask', json={'question': '123 Main Street'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['response'], 'The price is 568,000 dollars')

    def test_ask_no_question_Bad_Request(self):
        response = self.app.post('/ask', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Bad Request: Question is required')
