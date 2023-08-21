import sqlite3
from pathlib import Path

from flask import app

from chatbot.Exceptions.InternalServiceException import InternalServiceException


class DatabaseAccessor:

    def __init__(self):
        current_dir = Path(__file__).parent.parent
        self.db_path = current_dir / 'database/properties.db'
        app.logging.info(f"Database path: {self.db_path}")

    def run_query(self, query, args=()):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute(query, args)
                return c
        except sqlite3.Error as e:
            app.logging.error(f"Database error: {e}")
            raise InternalServiceException(f"Database error: {e}")

    def get_context_from_db(self, question) -> str:
        keyword = self.extract_keyword(question)
        if not keyword:
            return "context: We don't have the info about this property"
        else:
            context_query = "SELECT context FROM property_data WHERE keyword = ?"
            return self.run_query(context_query, (keyword,)).fetchone()[0]

    def extract_keyword(self, question):
        # Logic to extract the keyword from the question
        keywords_query = "SELECT keyword FROM property_data"
        query_return = self.run_query(keywords_query).fetchall()
        return next((keyword for (keyword,) in list(query_return) if keyword in question), None)
