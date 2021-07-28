import os
from fastapi import FastAPI
import requests

app = FastAPI()

def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Referer": "https://weibo.com"
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    time.sleep(3)   # 加上3s 的延时防止被反爬
    return response.text

@app.get("/")
async def index():
	url= "https://raw.githubusercontent.com/Jboobs/deploy/main/LICENSE"
	LICENSE = get_html(url)
	#name = os.getenv("NAME", "world")
	return LICENSE

@app.get("/ip")
async def index():
	url= "https://api.ip.sb/ip"
	ip = get_html(url)
	return response
