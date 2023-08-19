import logging
import sqlite3
import properties_data


class DatabaseCreator:
    def __init__(self, db_path='../../property_data.db'):
        self.db_path = db_path

    def create_database(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()

            with conn:
                # Check if the table already exists
                c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='properties'")
                if c.fetchone() is None:
                    # Create the table, UNIQUE will ensure that no two properties have the same address
                    c.execute('''CREATE TABLE properties (address text UNIQUE, description text)''')

                    # INSERT OR IGNORE will skip any records that would cause a duplicate key error
                    c.executemany("INSERT OR IGNORE INTO properties (address, description) VALUES (?, ?)",
                                  properties_data.PROPERTIES_DATA)

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
