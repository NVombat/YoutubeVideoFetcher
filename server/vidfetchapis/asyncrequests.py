# https://developers.google.com/youtube/v3/sample_requests

from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import asyncio
import httpx
import os

load_dotenv()

key = os.getenv("API_KEY")

weeks = input("How Many Weeks Prior To The Current Date Do You Want Results For: ")
search_query = input("What Are You Looking For: ")

part = "snippet"
order = "date"
type = "video"

from_date = datetime.utcnow() - timedelta(weeks=10)
vid_date = from_date.replace(microsecond=0).isoformat("T") + "Z"
publishedAfter = vid_date

client = requests.Session()

base_url = "https://www.googleapis.com/youtube/v3/search"
url = (
    base_url
    + "?key="
    + key
    + "&part=snippet&oder=date&type=video&q="
    + search_query
    + "&publishedAfter="
    + publishedAfter
)

response = client.get(url=url)
content = response.content.decode()
content.replace("\n", "")
print(content)
print(response.status_code)


# async def http_call_async():
#     for num in range(1, 10):
#         await asyncio.sleep(1)
#         print(num)
#     async with httpx.AsyncClient() as client:
#         r = await client.get("https://www.googleapis.com/youtube/v3/search")
#         print(r)
