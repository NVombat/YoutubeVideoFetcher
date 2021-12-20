#RESOURCE - https://github.com/googleapis/google-api-python-client -> DOCS

from googleapiclient.discovery import build
from datetime import datetime, timedelta
from rest_framework import status
from django.http import response
from dotenv import load_dotenv
import os

from . import Fetched_Data

load_dotenv()

def fetch_vid_data(request, **kwargs) -> response.JsonResponse:
    """
    Fetches video data using the YouTube API when hit with GET requests

    Args:
        request
        **kwargs

    Returns:
        response.JsonResponse
    """
    try:
        print("GET REQUEST")
        print("Request Object DATA:", request.data)

        search_query = request.data.get("Query")
        weeks = request.data.get("Weeks")

        print(search_query, weeks)

        youtube_service = build('youtube', 'v3', developerKey=os.getenv("API_KEY"))

        # From Which Date Are Results Wanted
        from_date = datetime.utcnow() - timedelta(weeks=weeks)
        vid_date = from_date.replace(microsecond=0).isoformat("T") + "Z"

        print(vid_date)

        request = youtube_service.search().list(
            part="snippet",
            order="date",
            type="video",
            publishedAfter=vid_date,
            q=search_query,
        )

        storage_dict = {}

        response = request.execute()
        res_data = response["items"]
        print(res_data)

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

        search_query = search_query.upper()
        storage_dict[search_query] = video_data

        Fetched_Data.insert_data(search_query, storage_dict)

        youtube_service.close()

        return response.JsonResponse(
            {"success_status": True},
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        print(e)
        return response.JsonResponse(
            {"error": "Error Occured While Fetching Data", "success_status": False},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


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
    pass
