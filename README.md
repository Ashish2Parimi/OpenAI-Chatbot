# Chatbot Project
A comprehensive chatbot that helps users with various tasks. This repository contains all the code, unit tests, and necessary files to get the chatbot up and running.


### Installation
##### For execute the following commands in a pre-existing  virtual environment in an IDE like Pycharm to install dependencies, run unit tests, create the database, and start the bot.

### Usage
Once the bot is running, you can interact with it using default port is 5000 following commands:
#### Postman
```
POST : http://localhost:5000/ask

headers: Content-Type: application/json

body: {
    "question":"How many rooms does the house at 123 Main Street have?"
}
```
#### Curl
```
curl -X POST -H "Content-Type: application/json" -d '{"question":"How many rooms does the house at 123 Main Street have?"}' http://localhost:5000/ask
```


### Structure
```
chatbot/: Main chatbot code.
-- bot.py/: Code for the bot's functionality.
-- config.py/: Configuration file for the API, DB, LLM-Model.
-- database/
-- -- create_database.py
-- -- properties_data.py : Data for the database.
test/
-- test_bot.py/
-- database/
-- -- test_database.py/
requirements.txt: File containing the required Python packages.
run.py: Main run script to install dependencies, run unit tests, create the database, and start the bot.
```

