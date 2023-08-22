import sqlite3
import unittest
from unittest.mock import patch, Mock

from chatbot.accessor.DatabaseAccessor import DatabaseAccessor
from chatbot.exceptions.InternalServiceException import InternalServiceException


class TestDatabaseAccessor(unittest.TestCase):

    def setUp(self):
        self.db_accessor = DatabaseAccessor()

    @patch('sqlite3.connect')
    def test_run_query_success(self, mock_connect):
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [('result',)]
        mock_connect.return_value.cursor.return_value = mock_cursor

        query = "SELECT * FROM property_data"
        results = self.db_accessor.run_query(query)
        mock_cursor.execute.assert_called_with(query, ())
        self.assertEqual(results, [('result',)])

    @patch('sqlite3.connect')
    def test_run_query_sqlite_error(self, mock_connect):
        mock_connect.side_effect = sqlite3.Error('An error occurred')

        with self.assertRaises(InternalServiceException):
            self.db_accessor.run_query("SELECT * FROM property_data")

    @patch('chatbot.accessor.DatabaseAccessor.DatabaseAccessor.run_query')
    def test_extract_keyword(self, mock_run_query):
        mock_run_query.return_value = [('keyword1',), ('keyword2',)]
        question = "Information about keyword1"

        keyword = self.db_accessor.extract_keyword(question)
        self.assertEqual(keyword, 'keyword1')

    @patch('chatbot.accessor.DatabaseAccessor.DatabaseAccessor.run_query')
    def test_get_context_from_db(self, mock_run_query):
        mock_run_query.side_effect = [
            [('keyword1',)],
            [('context1',)]
        ]
        question = "Information about keyword1"

        context = self.db_accessor.get_context_from_db(question)

        self.assertEqual(context, 'context1')

    @patch('chatbot.accessor.DatabaseAccessor.DatabaseAccessor.run_query')
    def test_get_context_from_db_no_keyword(self, mock_run_query):
        mock_run_query.return_value = [('keyword1',), ('keyword2',)]
        question = "Information about unknown_keyword"

        context = self.db_accessor.get_context_from_db(question)

        self.assertEqual(context, "context: We don't have the info about this property")

