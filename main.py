import os
from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
async def index():
	url= "https://raw.githubusercontent.com/Jboobs/deploy/main/LICENSE"
	response = requests.get(url).text
	name = os.getenv("NAME", "world")
	return response
