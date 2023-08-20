import json
import logging
import sqlite3
from pathlib import Path


class DatabaseCreator:
    def __init__(self, db_path='property_data.db'):
        self.db_path = db_path

    def create_database(self):
        conn = None
        data_dir = Path(__file__).parent.parent.parent / 'data.json'
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            with conn:
                # Check if the table already exists
                c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='properties'")
                if c.fetchone() is None:
                    # Create the table, UNIQUE will ensure that no two properties have the same address
                    c.execute('''CREATE TABLE properties (address text UNIQUE, description text)''')
                    with open(data_dir, 'r') as file:
                        properties_data = json.load(file)
                        data = [(item['address'], item['description']) for item in properties_data]
                    # INSERT OR IGNORE will skip any records that would cause a duplicate key error
                    c.executemany("INSERT OR IGNORE INTO properties (address, description) VALUES (?, ?)",
                                  data)

            logging.info("Database created successfully.")

        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")

        finally:
            if conn:
                conn.close()

    def create(self):
        self.create_database()


if __name__ == '__main__':
    db_creator = DatabaseCreator()
    db_creator.create()
