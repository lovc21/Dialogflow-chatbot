import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google.oauthb2.credentials import Credentials

import dialogflow_v2 as dialogflow

# Set the credentials and project information
credentials = Credentials.from_service_account_file('path/to/service_account.json')
session_client = dialogflow.SessionsClient(credentials=credentials)
project_id = 'your-project-id'

# Set the telegram bot information
TOKEN = 'your-bot-token'

def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same session_id between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    for text in texts:
        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)
        return response.query_result.fulfillment_text

def start(bot, update):
    """Start the bot and display the welcome message."""
    update.message.reply_text('Hello! Welcome to my Dialogflow chatbot.')

def chat(bot, update):
    """Handle the user's message and reply with the Dialogflow response."""
    user_text = update.message.text
    session_id = update.message.chat_id
    response = detect_intent_texts(project_id, session_id, [user_text], 'en')
    update.message.reply_text(response)

def main():
    """Start the bot."""
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, chat))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
