# Chatbot Project

---
This project is a chatbot that answers questions about a house. The chatbot uses OpenAI's GPT-3 API to generate responses. The chatbot is built using Python and Flask. The chatbot is deployed on a local server and can be accessed using Postman or Curl. 

---
### Requirements
```
Python >= 3.9
```
#### Note: OpenAI API key is part of ``chatbot/config/OpenAI_config.env``. Provide the key if required.

### Installation
Open terminal and navigate to the code directory. Follow the commands in terminal ( macOs tested) to give permissions to ``run.py``, install dependencies, run unit tests, create the database, and start the bot.
```
!export PYTHONPATH=$PWD 
chmod +x ./run.py
./run.py
```

---
### API Docs
```
parameters:

  name: question
    in: body
    type: string
    required: true
    default: "How many rooms does the house at 123 Main Street have?"
    description: The question asked by the user
```
```
responses:

  200:
    description: The response from the bot answering the question
  400:
    description: Bad Request - Question is required
  500:
    description: Internal Server Error - Unable to reach database, OpenAI API, or other internal error
```

**Example**:

**Question**: "How many rooms does the house at 123 Main Street have?"

**Chatbot** Response: "The house at 123 Main Street has 3 bedrooms."

### Note: Check ``chatbot/database/data.json`` for more examples to frame questions

---


### Usage
Once the bot is running, you can interact with it using default port(5000) following commands:

#### Postman

* Method : POST 

* URL : http://127.0.0.1:5000/prompt

* headers: ``Content-Type: application/json``

* body:  ```"question":"How many rooms does the house at 123 Main Street have?" ```

#### Curl
```
curl -X POST -H "Content-Type: application/json" -d '{"question":"How many rooms does the house at 123 Main Street have?"}' http://127.0.0.1:5000/prompt
```
##### Response
```
{
    "response": "The house at 123 Main Street has 3 bedrooms",
}
```
### Observations
403 - Forbidden Exception in Postman
```
    description: Forbidden - Unable to  access chatbot directory from current location
    
    resolution: Navigate to the chatbot directory, re-run the script and relaunch postman. try curl command if issue persists
```



