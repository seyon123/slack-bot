# For Slack
import slack
from slackeventsapi import SlackEventAdapter

# Store Keys
from dotenv import load_dotenv

import os
from pathlib import Path
from datetime import datetime
import random
import requests
import json

# To handle requests
from flask import Flask

# Load the .env file and read values
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
SIGNING_SECRET = os.environ['SIGNING_SECRET']
SLACK_TOKEN = os.environ['SLACK_TOKEN']
WEATHER_SECRET=os.environ['WEATHER_SECRET']

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
    event = payload.get('event',{})
    channel_id = event.get('channel')
    user_id = event.get('user')

    #Get the user's username
    user_info = client.users_info(user=user_id)
    username = user_info["user"]["real_name"]

    #Make sure we aren't talking to a bot
    if "bot" not in username.lower():
        msg = event.get('text')

        if THIS_BOT_ID != user_id:
            msg_strip = msg.strip()
            print(msg_strip)
            # Response when userr aska a question
            if msg_strip[-1] == "?":
                messages = ["wow!", "that's actually crazy.", "you sound like a Toronto manz.", "hmm.", "you are amazing.", "yo fam.", "OH MY GOSH!", "I know I am awesome... but.." ]
                client.chat_postMessage(channel=channel_id, text="<@" + user_id + "> "+random.choice(messages)+" You asked me:")
                client.chat_postMessage(channel=channel_id, text=msg)
            # Response to weather
            elif ("Weather in").lower() in msg.lower():
                try:
                    city = msg.split("in ",1)[1]
                    weather_api = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=metric&appid=" + WEATHER_SECRET
                    print(weather_api)
                    request = requests.get(weather_api)
                    response = json.loads(request.text)
                    print(response)
                    message="City: " + response["name"] + "\nWeather: " + (response["weather"][0])["main"] + "\nTemperature: " + str((response["main"])["temp"]) + "°C" + "\nFeels Like: " + str((response["main"])["feels_like"]) + "°C"
                    client.chat_postMessage(channel=channel_id, text=message)
                except Exception as err:
                    print(f'An Error Occurred: {err}')

#Start the flask webserver
if __name__ == "__main__":
    app.run(debug=True)
