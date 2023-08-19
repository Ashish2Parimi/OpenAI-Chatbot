import sqlite3
import unittest
from unittest.mock import MagicMock, patch

from chatbot.database.create_database import DatabaseCreator


class TestDatabaseCreator(unittest.TestCase):

    def setUp(self):
        self.db_creator = DatabaseCreator()

    @patch("sqlite3.connect")
    def test_create_database_table_exists(self, mock_connect):
        # Mock the cursor fetchone method to simulate that the table already exists
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = True

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        self.db_creator.create_database()

        # Assert that the CREATE TABLE command was never executed
        self.assertEqual(mock_cursor.execute.call_count, 1)

    @patch("sqlite3.connect")
    def test_create_database_table_does_not_exist(self, mock_connect):
        # Mock the cursor fetchone method to simulate that the table does not exist
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        self.db_creator.create_database()

        # Assert that the CREATE TABLE command was executed
        self.assertEqual(mock_cursor.execute.call_count, 2)
        mock_cursor.execute.assert_any_call('''CREATE TABLE properties (address text UNIQUE, description text)''')

    @patch("sqlite3.connect")
    @patch("logging.error")
    def test_create_database_error(self, mock_log_error, mock_connect):
        mock_connect.side_effect = sqlite3.Error("An error occurred")
        self.db_creator.create_database()
        mock_log_error.assert_called_with("Database error: An error occurred")
