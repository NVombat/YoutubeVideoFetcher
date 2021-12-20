from django.http import response
from dotenv import load_dotenv
from typing import Dict
import pymongo
import os

from .errors import KeywordNotFoundError
from core.settings import DATABASE

load_dotenv()


class VideoFetchData:
    def __init__(self) -> None:
        """
        Connect to MongoDB
        """
        client = pymongo.MongoClient(DATABASE["mongo_uri"])
        self.db = client[DATABASE["db"]][os.getenv("DATA_COLLECTION")]

    def insert_data(self, search_query: str, video_data: Dict[Dict[str, str, str, Dict[str, str, str]]]) -> None:
        """Insert search query and video data into db

        Args:
            search_query: Search Text
            video_data: Data Extracted from API

        Returns:
            None
        """
        if self.db.find_one({search_query: {"$exists":1}}):
            print("SEARCH QUERY EXISTS - UPDATE ENTRY")
            pass
        else:
            print("SEARCH QUERY DOES NOT EXIST - CREATE NEW ENTRY")
            self.db.insert_one(video_data)

    def fetch_user_data(self, search_query: str) -> response.JsonResponse:
        """Fetches specific data from db based on keyword (query)

        Args:
            search_query: Search Text

        Returns:
            response.JsonResponse
        """
        if data := self.db.find(
            {search_query: {"$exists":1}},
            {
                "_id": 0,
            },
        ):
            data.sort("publish_date", -1)
            docs = list(data)
            json_data = response.JsonResponse(docs, safe=False)
            return json_data

        raise KeywordNotFoundError(f"Data For {search_query} Not Found In Database - Fetching Data Please Wait While We Return Your Results")
        #While Excepting run API again
