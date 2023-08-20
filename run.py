#!/usr/bin/env python3


import logging
import subprocess


def install_requirements():
    logging.info("Installing required packages...")
    subprocess.run(["pip3", "install", "-r", "requirements.txt"])


def run_unit_tests():
    logging.info("Running unit tests...")
    # Replace this with the correct path to your unit tests
    path_to_tests = "test/"
    result = subprocess.run(["python3", "-m", "unittest", "discover", path_to_tests, "-v"])
    return result.returncode


def create_database():
    logging.info("Creating database...")
    subprocess.run(["python3", "chatbot/database/create_database.py"])


def start_bot():
    logging.info("Starting the bot...")
    subprocess.run(["python3", "chatbot/bot.py"])


def main():
    install_requirements()

    test_result = run_unit_tests()
    if test_result == 0:
        logging.info("Unit tests passed. \nCreating Database...")
        create_database()
        logging.info("Starting the bot...")
        start_bot()
    else:
        logging.info("Unit tests failed. Please fix the errors before running the bot.")


if __name__ == "__main__":
    main()
