# Chatbot Project
A comprehensive chatbot that helps users with various tasks. This repository contains all the code, unit tests, and necessary files to get the chatbot up and running.

#### Requirements
```
Python >= 3.9
```
#### Note: OpenAI API key is included as part of ``config.env``

### Installation
##### Open a terminal( maxOs ) in the code directory and execute the following commands to install dependencies, run unit tests, create the database, and start the bot.
```
chmod +x ./run.py
./run.py
```

### Usage
Once the bot is running, you can interact with it using default port is 5000 following commands:
#### Postman
```
POST : http://127.0.0.1:5000/prompt

headers: Content-Type: application/json

body: {
    "question":"How many rooms does the house at 123 Main Street have?"
}
```
#### Curl
```
curl -X POST -H "Content-Type: application/json" -d '{"question":"How many rooms does the house at 123 Main Street have?"}' http://127.0.0.1:5000/prompt
```
##### Response
```
{
    "answer": "The house at 123 Main Street has 3 bedrooms",
    
}
```




