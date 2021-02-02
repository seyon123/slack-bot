# For Slack
import slack
from slackeventsapi import SlackEventAdapter

# Store Keys
from dotenv import load_dotenv

import os
from pathlib import Path
from datetime import datetime
import random

# To handle requests
from flask import Flask

# Load the .env file and read values
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
SIGNING_SECRET = os.environ['SIGNING_SECRET']
SLACK_TOKEN = os.environ['SLACK_TOKEN']

#Create the flask application
app = Flask(__name__)

#Configure the flask app to connect with Slack
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET,'/slack/events', app)
client = slack.WebClient(token=SLACK_TOKEN)

#
THIS_BOT_ID = client.api_call("auth.test")['user_id']


#Generic function to send a message
def message(msg, channel_id):
    client.chat_postMessage(channel=channel_id, text=str(msg))

#Send a welcome message on start
now = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
message("["+ now + "] Bot started on this channel.", "ram-bot")

#What to do when a message is recieved
# handling Message Events
@slack_event_adapter.on('message')
def message(payload):
    print("got message")
    event = payload.get('event',{})
    channel_id = event.get('channel')
    user_id = event.get('user')

    #Get the user's username
    user_info = client.users_info(user=user_id)
    username = user_info["user"]["real_name"]

    #Make sure we aren't talking to a bot
    if "bot" not in username.lower():
        print("past bot test")
        msg = event.get('text')

        if THIS_BOT_ID != user_id:
            print("past self check")
            messages = ["wow!", "that's actually crazy.", "you sound like a Toronto manz.", "hmm.", "you are amazing.", "yo fam.", "OH MY GOSH!", "I know I am awesome... but.." ]
            client.chat_postMessage(channel=channel_id, text="<@" + user_id + "> "+random.choice(messages)+" You said:")
            client.chat_postMessage(channel=channel_id, text=msg)

#Start the flask webserver
if __name__ == "__main__":
    app.run(debug=True)
