# Dialogflow-chatbot

This is a simple chatbot that is used for providing directions and transportation information in Ljubljana, Slovenia, based on the current weather conditions. The chatbot uses Dialogflow for natural language processing and understanding, and it is built using the Flask web framework. The data for the weather conditions is stored in a MongoDB Atlas database, and the chatbot uses the PyMongo library to interact with the database.



## Used libraries:

  Json   
  Flask      
  Pymongo   
  Certifi  
  
## How to setup
To set up the chatbot, you will need to:

  1. Clone the repository 
  2. Install the required libraries (Json, Flask, PyMongo, Certifi)
  3. Set up a Dialogflow agent and import the settings from the Dialogflow agent directory.
  4. import the Dialogflow agent settings from dialogflow agent directori  
  5. Copy the username and password from MongoDB Atlas and paste them into the config.json file.
  6. Start ngrok by typing "ngork http 5000" in the terminal.
  7. Copy the https url provided by ngrok and paste it into the Dialogflow Fulfillment tab, adding "/webhook" at the end.
  8. Start the FlaskServer.py script to run the chatbot.
  
___
It is important to note that you will need to have the appropriate dependencies installed on your computer and have a Dialogflow account to set up the agent and access the settings. Also, it is important to follow the instructions provided in the repository, as well as the instructions provided in the libraries' documentation to ensure the successful execution of the script and proper communication with the Dialogflow agent and MongoDB Atlas.




