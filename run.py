#!/usr/bin/env python3

import subprocess
from logging.config import dictConfig
from pathlib import Path

from flask import app

"""
This is the main entry point for the chatbot. It will install the required packages, run the unit tests, create the
database, and start the chatbot.
"""
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def install_requirements():
    app.logging.info("Installing required packages...")
    subprocess.run(["pip3", "install", "-r", "requirements.txt"])


def run_unit_tests():
    app.logging.info("Running unit tests...")
    path_to_tests = Path(__file__).parent / 'test'
    print(path_to_tests)
    result = subprocess.run(["python3", "-m", "unittest", "discover", path_to_tests, "-v"])
    return result.returncode


def create_database():
    app.logging.info("Creating database...")
    subprocess.run(["python3", "chatbot/database/CreateDatabase.py"])


def start_bot():
    subprocess.run(["python3", "chatbot/agent/Agent.py"])


def main():
    install_requirements()

    test_result = run_unit_tests()
    if test_result == 0:
        create_database()
        app.logging.info("Database created. Unit tests passed.")
        app.logging.info("Starting the chatbot...")
        start_bot()
    else:
        app.logging.error("Unit tests failed. Please fix the errors before running the bot.")


if __name__ == "__main__":
    main()
