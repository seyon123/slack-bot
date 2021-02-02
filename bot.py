# For Slack connections
import slack
from slackeventsapi import SlackEventAdapter

# Store Keys
from dotenv import load_dotenv

#Some other tools
import os
from pathlib import Path
from datetime import datetime

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
