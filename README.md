# Dialogflow-chatbot
This is a simple chatbot that is used for getting directions and transport methods in ljubljana on the basis of wether in the city.

## Used libraries:

  Json   
  Flask      
  Pymongo   
  Certifi  
  
## How to setup

  1. Clone the repository  
  2. Install the libraries  
  3. Set up the Dialogflow agent  
  4. import the Dialogflow agent settings from dialogflow agent directori  
  5. Install ngrok  
  6. Set up the Mongodb Atlas
  7. Copy the user name and password  form Mongodb Atlas in to the config.json 
  8. Start ngrok and type "ngork http 5000" 
  9. Copy the https url that ngrok makes and paste it in the Dialogflow Fulfillment tab, add "/webhook" at the end
  10. Start the script FlaskServer.py
