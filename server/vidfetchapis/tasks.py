# RESOURCE - https://github.com/googleapis/google-api-python-client -> DOCS

from celery.utils.log import get_task_logger
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from rest_framework import status
from django.http import response
from celery import shared_task
from dotenv import load_dotenv
import requests
import os

from .errors import KeywordNotFoundError
from . import Fetched_Data

logger = get_task_logger(__name__)
load_dotenv()

curr_key = 0
api_keys = os.getenv("API_KEY").split(" ")
print(api_keys)
youtube_service = build("youtube", "v3", developerKey=api_keys[0])


def switch_api_keys() -> None:
    """
    If provided with more than 1 API Keys, when 1 Key
    is exhausted, switches to the other keys till all
    keys are exhausted

    Returns:
        None
    """
    global curr_key

    num_of_keys = len(api_keys)

    if num_of_keys == 1:
        logger.info("No More API Keys, Only 1 API Key Was Available")
        return

    global youtube_service

    # Use keys one after another
    if num_of_keys - 1 > curr_key:
        curr_key = curr_key + 1
    # When all keys are used go back to first key
    elif num_of_keys - 1 == curr_key:
        curr_key = 0

    youtube_service = build("youtube", "v3", developerKey=api_keys[curr_key])
    logger.info("Swicthed API Keys If Feasable")


@shared_task
def fetch_vid_data(request=None, *args, **kwargs) -> bool:
    """
    Fetches video data using the YouTube API when hit with GET requests
    Also a shared task run every 45 seconds with hardcoded data

    Args:
        request=None (Default)
        *args
        **kwargs

    Returns:
        bool
    """
    try:
        if request:
            print("GET REQUEST")
            print("Request Object DATA:", request.query_params)

            search_query = request.query_params.get("Query")
            weeks = request.query_params.get("Weeks")
            weeks = int(weeks)
            print(search_query, weeks)

            logger.info("Successfully Retrieved Request Information")

        else:
            search_query = args[0]
            weeks = args[1]
            logger.info("Successfully HardCoded Search Information")

        # From Which Date Are Results Wanted
        from_date = datetime.utcnow() - timedelta(weeks=weeks)
        vid_date = from_date.replace(microsecond=0).isoformat("T") + "Z"
        print(vid_date)

        req = youtube_service.search().list(
            part="snippet",
            order="date",
            type="video",
            publishedAfter=vid_date,
            q=search_query,
        )
        try:
            res = req.execute()
            logger.info("Successfully Connected to YouTube via API")

        except Exception:
            logger.info("Error while Connecting to API")
            switch_api_keys()
            return

        res_data = res["items"]
        logger.info("Successfully Fetched Data from Request")

        video_data = {}

        for items in res_data:
            vid_data = items["snippet"]

            publish_date = vid_data["publishedAt"]
            title = vid_data["title"]
            description = vid_data["description"]
            channel = vid_data["channelTitle"]

            thumbnail_data = vid_data["thumbnails"]
            default_thumbnail = thumbnail_data["default"]
            default_url = default_thumbnail["url"]
            medium_thumbnail = thumbnail_data["medium"]
            medium_url = medium_thumbnail["url"]
            high_thumbnail = thumbnail_data["high"]
            high_url = high_thumbnail["url"]

            thumbnail_urls = {}
            thumbnail_urls["default"] = default_url
            thumbnail_urls["medium"] = medium_url
            thumbnail_urls["high"] = high_url

            data = {}
            data["title"] = title
            data["description"] = description
            data["channel"] = channel
            data["thumbnail_urls"] = thumbnail_urls

            video_data[publish_date] = data

        logger.info("Successfully Created Data to be Stored")
        search_query = search_query.upper()
        Fetched_Data.insert_data(search_query, video_data)
        logger.info("Successfully Stored Data from API")

        youtube_service.close()
        logger.info("Successfully Completed Process using API")

        return True

    except Exception as e:
        print(e)
        logger.info("Error in Fetching Data from API")
        return False


def get_paginated_data(request, **kwargs) -> response.JsonResponse:
    """
    Gets Data from database when hit with GET requests & returns
    paginated responses

    Args:
        request
        **kwargs

    Returns:
        response.JsonResponse
    """
    try:
        print("GET REQUEST")
        print("Request Object DATA:", request.data)

        search_query = request.query_params.get("Query")
        print(search_query)

        searchquery = search_query.upper()
        data = Fetched_Data.fetch_user_data(searchquery)

        return data

    except KeywordNotFoundError:
        api_url = "http://127.0.0.1:8000/api/fetchvids"
        client = requests.Session()
        payload = {"Query": search_query, "Weeks": 10}
        client.get(url=api_url, params=payload)

        get_data_url = "http://127.0.0.1:8000/api/getdata"
        params = {"Query": search_query}
        client.get(url=get_data_url, params=params)

    except Exception as e:
        print(e)
        return response.JsonResponse(
            {"error": "Error Occured While Getting Data", "success_status": False},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
