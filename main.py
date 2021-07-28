from flask import Flask
from flask_websocket import WebSocket

app = Flask(__name__)
ws = WebSocket(app)


@ws.on_raw_message
def raw_message_handler(message):
print(message)
