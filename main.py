import os
from fastapi import FastAPI
import requests

app = FastAPI()

def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Referer": "https://weibo.com"
    }
    response = requests.get(url, headers=headers)
    return response.text

@app.get("/")
async def index():
	url= "https://raw.githubusercontent.com/Jboobs/deploy/main/LICENSE"
	response = get_html(url)
	#name = os.getenv("NAME", "world")
	return response

@app.get("/ip")
async def index():
	url= "https://api.ip.sb/ip"
	response = get_html(url)
	return response
