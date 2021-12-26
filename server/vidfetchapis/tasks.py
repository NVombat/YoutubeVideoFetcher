# RESOURCE - https://github.com/googleapis/google-api-python-client -> DOCS

from celery.utils.log import get_task_logger
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from rest_framework import status
from django.http import response
from celery import shared_task
from dotenv import load_dotenv
from math import ceil
import requests
import os

from .errors import KeywordNotFoundError, PageNotFoundError
from .utils import convert_data_to_storable_format
from . import Fetched_Data

logger = get_task_logger(__name__)
ITEMS_PER_PAGE = 2
load_dotenv()

curr_key = 0
api_keys = os.getenv("API_KEY").split(" ")
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
        logger.info("Used All API Keys - Moving Back To First API Key")

    youtube_service = build("youtube", "v3", developerKey=api_keys[curr_key])
    logger.info("Swicthed API Keys If Feasable")


def get_next_page_data(req, res: dict, query: str) -> None:
    """
    Recursive Function To Fetch Data From The Pages Following
    The First Page Till No Pages Remain

    Args:
        req: Previous Request
        res: Previous Response

    Returns:
        None (Else Recursive)
    """
    next_page_req = youtube_service.search().list_next(req, res)

    try:
        next_page_res = next_page_req.execute()
        logger.info("Successfully Connected to YouTube via API")
    except Exception:
        logger.info("Error while Connecting to API")
        switch_api_keys()
        return

    logger.info("Fetching Next Page Data")

    if next_page_res == None:
        logger.info(f"Next Page Does Not Exist - No More Data For {query}")
        return
    else:
        video_data = convert_data_to_storable_format(next_page_res)
        logger.info("Successfully Created Data to be Stored")
        Fetched_Data.insert_data(query, video_data)
        logger.info("Successfully Stored Data from API")

        prev_req = next_page_req
        prev_res = next_page_res

        logger.info("Moving On To Next Page")
        get_next_page_data(prev_req, prev_res, query)


@shared_task
def fetch_vid_data(request=None, *args, **kwargs) -> bool:
    """
    Fetches video data using the YouTube API when hit with GET requests
    Also a shared task which runs every 45 seconds with hardcoded data

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

        logger.info("Successfully Fetched Data from Request")

        video_data = convert_data_to_storable_format(res)
        logger.info("Successfully Created Data to be Stored")
        search_query = search_query.upper()
        Fetched_Data.insert_data(search_query, video_data)
        logger.info("Successfully Stored Data from API")

        logger.info("Fetching Next Page Data")
        get_next_page_data(req, res, search_query)

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
        print("Request Object DATA:", request.query_params)

        page = int(request.query_params.get("Page"))
        search_query = request.query_params.get("Query")
        print(page, search_query)

        searchquery = search_query.upper()
        data = Fetched_Data.fetch_user_data(searchquery)

        total_docs = len(data)
        print(len(data))

        # If Page Number Does Not Exist
        if page <= 0 or page > ceil(total_docs / ITEMS_PER_PAGE):
            raise PageNotFoundError("This Page Does Not Exist")
        # If No Page Is Specified
        elif page == None:
            page = 1

        left_lim = (page - 1) * ITEMS_PER_PAGE
        right_lim = left_lim + 2
        print(left_lim, right_lim)

        if total_docs != 0:
            return response.JsonResponse(
                {
                    "currentPage": page,
                    "hasNextPage": ITEMS_PER_PAGE * page < total_docs,
                    "hasPreviousPage": page > 1,
                    "nextPage": page + 1,
                    "previousPage": page - 1,
                    "lastPage": ceil(total_docs / ITEMS_PER_PAGE),
                    "data": data[left_lim:right_lim],
                },
                status=status.HTTP_200_OK,
            )
        else:
            raise KeywordNotFoundError(
                f"Data For {search_query} Not Found In Database - Fetching Results For {search_query}. Please Try Again In A Moment"
            )

    except KeywordNotFoundError:
        api_url = "http://127.0.0.1:8000/api/fetchvids"
        client = requests.Session()
        payload = {"Query": search_query, "Weeks": 10}
        client.get(url=api_url, params=payload)

        get_data_url = "http://127.0.0.1:8000/api/getdata"
        params = {"Query": search_query}
        client.get(url=get_data_url, params=params)

    except PageNotFoundError as pnfe:
        return response.JsonResponse(
            {"error": str(pnfe), "success_status": False},
            status=status.HTTP_404_NOT_FOUND,
        )

    except Exception as e:
        print(e)
        return response.JsonResponse(
            {"error": "Error Occured While Getting Data", "success_status": False},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
