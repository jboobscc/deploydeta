import os
from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
async def index():
	url= "https://puzz.helenrdawson.workers.dev"
	response = requests.get(url).text
	name = os.getenv("NAME", "world")
	return response
