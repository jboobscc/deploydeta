from flask import Flask
import requests

app = Flask(__name__)

def get_html(url):
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
	response = requests.get(url, headers=headers)
	return response.text

@app.route('/', methods=["GET"])
def hello_world():
	return "Hello World"

@app.route('/ip', methods=["GET"])
def getip():
	url= "https://api.ip.sb/ip"
	response = get_html(url)
	return response


@app.route('/get', methods=["GET"])
def getip():
	url= "http://httpbin.org/get"
	response = get_html(url)
	return response
