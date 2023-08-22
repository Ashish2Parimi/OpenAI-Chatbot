import sqlite3
from pathlib import Path

from flask import app

from chatbot.exceptions.InternalServiceException import InternalServiceException


class DatabaseAccessor:

    def __init__(self):
        current_dir = Path(__file__).parent.parent
        self.db_path = current_dir / 'database/properties.db'
        app.logging.info(f"Database path: {self.db_path}")

    def run_query(self, query, args=()):
        """
        This method will run a query on the database and return the results.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute(query, args)
                return c.fetchall()
        except sqlite3.Error as e:
            app.logging.error(f"Database error: {e}")
            raise InternalServiceException(f"Database error: {e}")
        finally:
            if conn:
                conn.close()

    def get_context_from_db(self, question) -> str:
        """
        This method will query the database for the context if the keyword exists in the question and return it or
        return a default message if the keyword does not exist.
        """
        keyword = self.extract_keyword(question)
        if not keyword:
            return "context: We don't have the info about this property"
        else:
            context_query = "SELECT context FROM property_data WHERE keyword = ?"
            return self.run_query(context_query, (keyword,))[0][0]

    def extract_keyword(self, question):
        """
        This method will extract the keyword from the question if exists and return it or return None.
        """
        # Logic to extract the keyword from the question
        keywords_query = "SELECT keyword FROM property_data"
        query_return = self.run_query(keywords_query)
        return next((keyword for (keyword,) in list(query_return) if keyword in question), None)
