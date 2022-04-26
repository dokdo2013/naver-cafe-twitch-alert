import requests
import dotenv
import os


def send(msg):
    dotenv.load_dotenv()
    SLACK_URL = os.getenv('SLACK_URL')
    data = {'text': msg}
    r = requests.post(SLACK_URL, json=data)


