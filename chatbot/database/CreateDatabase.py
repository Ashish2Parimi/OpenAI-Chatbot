import json
import logging
import sqlite3
from pathlib import Path


class DatabaseCreator:
    def __init__(self):
        current_dir = Path(__file__).parent
        self.db_path = current_dir / 'properties.db'
        self.data_path = current_dir / 'data.json'

    def create_database(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            with conn:
                # Check if the table already exists
                c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='property_data'")
                if c.fetchone() is None:
                    # Create the table, UNIQUE will ensure that no two property_data have the same address
                    c.execute('''CREATE TABLE property_data (keyword text UNIQUE, context text)''')
                    with open(self.data_path, 'r') as file:
                        data = [(item['keyword'], item['context']) for item in json.load(file)]
                    # INSERT OR IGNORE will skip any records that would cause a duplicate key error
                    c.executemany("INSERT OR IGNORE INTO property_data (keyword, context) VALUES (?, ?)",
                                  data)

            logging.info("Database created successfully.")

        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")

    def create(self):
        self.create_database()


if __name__ == '__main__':
    db_creator = DatabaseCreator()
    db_creator.create()
