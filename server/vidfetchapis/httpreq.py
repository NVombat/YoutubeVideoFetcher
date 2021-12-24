# https://developers.google.com/youtube/v3/sample_requests

from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import os

load_dotenv()


def http_request() -> int:
    """
    Builds a url & sends an HTTP GET request with parameters

    Returns:
        int
    """
    key = os.getenv("API_KEY")

    # weeks = input("How Many Weeks Prior To The Current Date Do You Want Results For: ")
    # search_query = input("What Are You Looking For: ")
    search_query = "soccer"
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
        + "&part="
        + part
        + "&oder="
        + order
        + "&type="
        + type
        + "&q="
        + search_query
        + "&publishedAfter="
        + publishedAfter
    )

    res = client.get(url=url)
    content = res.content.decode()
    content.replace("\n", "")
    print(content)
    return res.status_code
