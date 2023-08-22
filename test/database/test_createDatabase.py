import unittest
from unittest.mock import patch, Mock

import sqlite3

from chatbot.database.CreateDatabase import DatabaseCreator


class TestDatabaseCreator(unittest.TestCase):

    def setUp(self):
        self.db_creator = DatabaseCreator()

    @patch('sqlite3.connect')
    @patch('json.load')
    @patch('builtins.open', new_callable=unittest.mock.mock_open,
           read_data='{"keyword": "value", "context": "context"}')
    def test_create_database_if_not_exist(self, mock_open, mock_json_load, mock_connect):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_json_load.return_value = [{'keyword': 'value', 'context': 'context'}]

        self.db_creator.create_database()

        mock_cursor.execute.assert_called_with('''CREATE TABLE property_data (keyword text UNIQUE, context text)''')
        mock_cursor.executemany.assert_called()

    @patch('sqlite3.connect')
    def test_not_create_database_if_exist(self, mock_connect):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = 'something'
        mock_connect.return_value.cursor.return_value = mock_cursor

        self.db_creator.create_database()

        mock_cursor.execute.assert_called_with(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='property_data'")
        mock_cursor.executemany.assert_not_called()

    @patch('sqlite3.connect')
    @patch('flask.app.logging.error')
    def test_handle_sqlite_error(self, mock_logging_error, mock_connect):
        mock_connect.side_effect = sqlite3.Error('An error occurred')

        self.db_creator.create_database()

        mock_logging_error.assert_called_with('Database error: An error occurred')


