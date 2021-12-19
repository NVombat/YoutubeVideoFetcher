from dotenv import load_dotenv
import pymongo
import os

from core.settings import DATABASE

load_dotenv()


class VideoFetchData:
    def __init__(self) -> None:
        """
        Connect to MongoDB
        """
        client = pymongo.MongoClient(DATABASE["mongo_uri"])
        self.db = client[DATABASE["db"]][os.getenv("DATA_COLLECTION")]

    def func(self,):
        pass
