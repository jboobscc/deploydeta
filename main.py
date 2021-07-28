from flask import Flask
from flask_websocket import WebSocket

app = Flask(__name__)
ws = WebSocket(app)

@ws.on('click')
def click(data):
print(data)
