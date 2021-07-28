import os
from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
async def index():
	url= "http://ip.sb"
	response = requests.get(url).text
	name = os.getenv("NAME", "world")
	return f"hello {response}!"
